# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 17:07:39 2019

@author: base7005
"""





from  geopy.geocoders import Nominatim
geolocator = Nominatim()
city ="London"
country ="Uk"
loc = geolocator.geocode(city+','+ country )
print("latitude is :-" ,loc.latitude,"\nlongtitude is:-" ,loc.longitude)



import requests
GOOGLE_MAPS_API_URL = 'http://maps.googleapis.com/maps/api/geocode/json'

params = {
    'address': 'oshiwara industerial center goregaon west mumbai',
    'sensor': 'false',
    'region': 'india'
}

# Do the request and get the response data
req = requests.get(GOOGLE_MAPS_API_URL, params=params)
res = req.json()

# Use the first result
result = res['results'][0]

geodata = dict()
geodata['lat'] = result['geometry']['location']['lat']
geodata['lng'] = result['geometry']['location']['lng']
geodata['address'] = result['formatted_address']

print('{address}. (lat, lng) = ({lat}, {lng})'.format(**geodata))