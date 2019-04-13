#!/usr/bin/python
# vim: set fileencoding=utf-8 :
# pylint: disable=E0401
# pylint: disable=C0103
"""
Geo coding proxy service
====
    $Id$  # nopep8
    $DateTime$ 04/11/2019
    $Author$ Sharad Bhadouria
    $Change$ 1
    $Reference$ https://wiki.python.org
"""

from BaseHTTPServer import BaseHTTPRequestHandler
import json
import urlparse
import requests
import config


class GeoCodingServiceDataProvider(object):
    """
    GeoCodingServiceDataProvider acts a public interface for outside world.
    Any new geo coding service MUST inherit from GeoCodingServiceDataProvider
    and implement to_json and get_url_params.
    New service also needs to be added to GEO_LOOKUP_SERVICES
    """

    def to_json(self, response):
        """
        gives the results in json format
        :param response: response of the http get request
        :return: results in json format
        """
        raise NotImplementedError

    def get_url_params(self, search):
        """
        gives the underlying url and the query params of the service in use
        :param search: the search used by the user
        :return: returns baseurl and the query params
        """
        raise NotImplementedError


class GoogleGeocodingServiceProvider(GeoCodingServiceDataProvider):
    """
    Google Geo coding service provider
    """
    def __init__(self, api_key):
        """
        init method for google geo coding
        :param api_key: key to access api
        """
        self.api_key = api_key
        self.baseurl = 'https://maps.googleapis.com/maps/api/geocode/json?'

    def to_json(self, response):
        """
        Google Geo coding service providers to json method.
        It checks the response and iterate over the results returned from the request
        :param response: response of the get request
        :return: Json formatted results
        """
        if response.ok:
            # parse the results and get the lat and lon key value
            json_response = response.json()
            if json_response['status'] == 'ZERO_RESULTS':
                return {"status": "OK", "data": "No results found"}
            if json_response['status'] != 'OK':
                return {"status": json_response['status'], "data": {}}
            return {"status": "OK", "data": json_response['results'][0]['geometry']['location']}

        raise response.raise_for_status()

    def get_url_params(self, search):
        """
        Given a search return the base url and the query params
        :param search: address specified by user
        :return: baseurl and query params
        """

        query_params = {
            'address': search,
            'key': self.api_key,
        }
        return self.baseurl, query_params


class HereGeocodingServiceProvider(GeoCodingServiceDataProvider):
    """
    Here Geo Coding service provider
    """

    def __init__(self, app_id, app_code):
        """
        init method for here geo coding
        :param app_id: app_id used for here api
        :param app_code: app_code used for here api
        """
        self.baseurl = 'https://geocoder.api.here.com/6.2/geocode.json?'
        self.app_id = app_id
        self.app_code = app_code

    def to_json(self, response):
        """
        Here Geo coding service providers to json method.
        It checks the response and iterate over the results returned from the request
        :param response: response of the get request
        :return: Json formatted results
        """

        if response.ok:
            json_response_view = response.json()['Response']['View']
            if not json_response_view:
                # no results found
                return {"status": "OK", "data": "No results found"}

            result = json_response_view[0]['Result'][0]
            location = result['Location']['DisplayPosition']
            return {"status": "OK",
                    "data": {"lat": location['Latitude'],
                             "lng": location['Longitude']}}

        raise response.raise_for_status()

    def get_url_params(self, search):
        """
        Given a search return the base url and the query params
        :param search: search specified by user
        :return: baseurl and query params
        """
        query_params = {
            'searchtext': search,
            'app_id': self.app_id,
            'app_code': self.app_code,
        }
        return self.baseurl, query_params


# Any new Geo data provider must be added to GEO_LOOKUP_SERVICES list
GEO_LOOKUP_SERVICES = [
    GoogleGeocodingServiceProvider(api_key=config.GOOGLE_API_KEY),
    HereGeocodingServiceProvider(app_id=config.HERE_APP_ID, app_code=config.HERE_APP_CODE)]


class GeoCodingServiceDriver(BaseHTTPRequestHandler):
    """
    Driver class for geo service
    """
    def send_code(self, http_status_code, response_data):
        """
        Response that client sees

        :param http_status_code:
        :param response_data:
        :return: sends the response to the client
        """
        self.send_response(http_status_code)
        self.send_header('Content-type', 'text/json;charset=utf-8')
        self.end_headers()
        self.wfile.write(response_data)

    def do_GET(self):
        """
        actual program driver method
        :return: result in json format
        """
        query_path = urlparse.urlparse(self.path)

        query = urlparse.parse_qs(query_path.query)
        if query:
            address = query['q'][0]
            for service in GEO_LOOKUP_SERVICES:
                base_url, payload = service.get_url_params(address)
                response = None
                try:
                    response = requests.get(base_url, params=payload)
                except requests.exceptions.RequestException as exception:
                    print(exception)
                    # if response is none we raise manual exception
                    if response is None:
                        raise Exception("Oops something went wrong. "
                                        "We didn't receive response from server")

                    response.raise_for_status()

                if response.ok:
                    results = service.to_json(response)
                    return self.send_code(200, json.dumps(results, indent=4))

        return self.send_code(404, json.dumps({"status": "No results found", "data": {}}, indent=4))
