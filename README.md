# Song Recommendation App with Spotify Web API

# App Overview 
Simple song recommendation search app utilizing Spotify's web API. The app takes artist and track as inputs and returns recommended songs and artists. For more info about recommendation api by spotify, please see [here](https://developer.spotify.com/documentation/web-api/reference/browse/get-recommendations/). 


# Run with Docker
Run Streamlit app with Docker: 

		docker build -t dannylee1020/spotify-recommendation .
		docker run -p 8501:8501 dannylee1020/spotify-recommendation:latest

Then visit [localhost:8501](https://localhost:8501) to view the app.


# Reference
[Spotify API](https://developer.spotify.com/documentation/web-api/)
<br>
[Streamlit](https://www.streamlit.io/)