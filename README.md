# GeoCodingProxy

Overview:

Geo coding proxy is a simple network service that can resolve the lat, lng coordinates for the address provided
by using third party geocoding services. This service can support multiple geocoding services.
It currently supports Google Geocoding API and HERE Geocoding API.



Prerequisite:

python 2.7

pip

The code was written in python 2.7


Setup:

1. Clone this repo

2. pip install -r requirements.txt

3. Edit config.py file with your api credentials and server details


How To Run The Service:

Run following command from terminal/command prompt to start the service:

python geo_coding_service.py

Once the service starts you will see something like "('Thu Apr 11 21:59:20 2019', 'Server Starts - localhost:8000')"


How To Use The Services API:

Request should be of the form http://localhost:8000/?q=san+francisco+dolores+park

You can directly run the url on any latest browser OR 

On another terminal/command prompt run following to see some results:

curl http://localhost:8000/?q=san+francisco+dolores+park

Response will be of format:

{
    "status": "OK", 
    "data": {
        "lat": 37.7596168, 
        "lng": -122.4269038
    }
}

Bad request will have a response:

{
    "status": "No results found", 
    "data": {}
}

Adding new service:

All service must derive from GeoCodingServiceDataProvider and must implement to_json and get_url_params.
