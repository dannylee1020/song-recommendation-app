import streamlit as st
import config
from api import SpotifyAPI
import time
import pandas as pd



def run():
	st.title('Song Recommendation with Spotify API')
	st.text('')
	st.subheader('Description')
	st.markdown('Simple song recommendation search utilizing Spotify\'s web API. Please provide both artist and track name to get accurate recommendations')

	artist = st.text_input('Artist')
	track = st.text_input('Track name')


	# get access to spotify api
	spotify = SpotifyAPI(config.CLIENT_ID, config.CLIENT_SECRET)
	acess_token = spotify.get_access_token()

	if st.button('Get Recommendation'):
		with st.spinner('Fetching data now...'):
			time.sleep(5)
			recommendation = spotify.get_recommendation(artist = artist, track = track)

			if recommendation == None:
				st.write('**Track not found on Spotify. It could be due to spelling errors or space issues **')
			else:
				st.write('**LET YO NEIGHBOR HEAR DIS. SHARING IS CARING :)**')
				return st.write(recommendation)





if __name__ == '__main__':

	run()