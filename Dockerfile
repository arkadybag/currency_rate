FROM python:3.7.2
ENV PYTHONUNBUFFERED 1
RUN mkdir /jibrel
COPY . /jibrel
WORKDIR /jibrel
EXPOSE 8000
RUN pip install -r /jibrel/deploy_assets/requirements.txt

#CMD ["python3", "/jibrel/manage.py", "migrate"]
