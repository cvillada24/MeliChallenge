FROM python:buster
RUN apt-get update
RUN apt-get install virtualenv -y
WORKDIR /melichallenge
RUN virtualenv venv
COPY . /melichallenge
RUN pip3 install -r requirement.txt
EXPOSE 4000
CMD ["python3", "./Challenge/appmeli.py"]