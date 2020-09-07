FROM python:3.7

WORKDIR /opt/spotify-recommendation

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app app/

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["app/app.py"]