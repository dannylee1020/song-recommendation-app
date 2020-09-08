FROM python:3.7

WORKDIR /opt/spotify-recommendation

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app app/


# for local build
#EXPOSE 8501
#ENTRYPOINT ["streamlit", "run"]
#CMD ["app/app.py"]


# for Heroku
CMD streamlit run app/app.py --server.port $PORT