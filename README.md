# GeoCodingProxy

Overview:

Geo coding proxy is a simple network service that can resolve the lat, lng coordinates for the address provided
by using third party geocoding services. This service can support multiple geocoding services.
It currently supports Google Geocoding API and HERE Geocoding API.


Configuration:

Default PORT is used is 8000 and Default HOST is localhost
Update line 23 and 24 in geo_coding_proxy.py


Prerequisite:

python 2.7
pip
The code was written in python 2.7


Setup:

1. Clone this repo

2. pip install -r requirements.txt


How To Run The Service:

Run following command from terminal/command prompt to start the service:

python geo_coding_service.py

Once the service starts you will see something like "('Thu Apr 11 21:59:20 2019', 'Server Starts - localhost:8000')"


How To Use The Services API:

Request should be of the form http://localhost:8000/?q=san+francisco+dolores+park

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
