# Automates getting review texts from the Google Maps Place API

import csv
import base64
import pandas
import streamlit as st
from urllib.request import urlopen
import json


@st.cache
def get(query, place_type, api_key):
    places_url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&type={place_type}&key={api_key}'
    places_response = urlopen(places_url)

    reviews = []
    for place in json.loads(places_response.read())['results']:
        if place['user_ratings_total'] > 0:
            place_id = place['place_id']
            details_url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}'
            details_response = urlopen(details_url)
            details = json.loads(details_response.read())
            for review in details['result']['reviews']:
                reviews.append(review['text'])

    return reviews


st.title('Get Google Reviews')
st.markdown('A simple Python demonstration of using [Streamlit](https://streamlit.io/) with the [Google Maps Places API](https://developers.google.com/maps/documentation/places/web-service/details) to get Reviews.')
api_key = st.text_input(
    'Google Maps API key')
query = st.text_input('Search query', '')
place_type = st.selectbox('Place type', ['accounting',
                                        'airport',
                                        'amusement_park',
                                        'aquarium',
                                        'art_gallery',
                                        'atm',
                                        'bakery',
                                        'bank',
                                        'bar',
                                        'beauty_salon',
                                        'bicycle_store',
                                        'book_store',
                                        'bowling_alley',
                                        'bus_station',
                                        'cafe',
                                        'campground',
                                        'car_dealer',
                                        'car_rental',
                                        'car_repair',
                                        'car_wash',
                                        'casino',
                                        'cemetery',
                                        'church',
                                        'city_hall',
                                        'clothing_store',
                                        'convenience_store',
                                        'courthouse',
                                        'dentist',
                                        'department_store',
                                        'doctor',
                                        'drugstore',
                                        'electrician',
                                        'electronics_store',
                                        'embassy',
                                        'fire_station',
                                        'florist',
                                        'funeral_home',
                                        'furniture_store',
                                        'gas_station',
                                        'gym',
                                        'hair_care',
                                        'hardware_store',
                                        'hindu_temple',
                                        'home_goods_store',
                                        'hospital',
                                        'insurance_agency',
                                        'jewelry_store',
                                        'laundry',
                                        'lawyer',
                                        'library',
                                        'light_rail_station',
                                        'liquor_store',
                                        'local_government_office',
                                        'locksmith',
                                        'lodging',
                                        'meal_delivery',
                                        'meal_takeaway',
                                        'mosque',
                                        'movie_rental',
                                        'movie_theater',
                                        'moving_company',
                                        'museum',
                                        'night_club',
                                        'painter',
                                        'park',
                                        'parking',
                                        'pet_store',
                                        'pharmacy',
                                        'physiotherapist',
                                        'plumber',
                                        'police',
                                        'post_office',
                                        'primary_school',
                                        'real_estate_agency',
                                        'restaurant',
                                        'roofing_contractor',
                                        'rv_park',
                                        'school',
                                        'secondary_school',
                                        'shoe_store',
                                        'shopping_mall',
                                        'spa',
                                        'stadium',
                                        'storage',
                                        'store',
                                        'subway_station',
                                        'supermarket',
                                        'synagogue',
                                        'taxi_stand',
                                        'tourist_attraction',
                                        'train_station',
                                        'transit_station',
                                        'travel_agency',
                                        'university',
                                        'veterinary_care',
                                        'zoo'])
go = st.button('Get Reviews')

if go:
    reviews = pandas.DataFrame(data=get(query, place_type, api_key), columns=[
        'Review'])
    st.subheader('Reviews')
    st.dataframe(reviews)

    csv = reviews.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a download="reviews.csv" href="data:file/csv;base64,{b64}">Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)


st.markdown('___')
st.markdown('by [CaliberAI](https://github.com/CaliberAI/)')
