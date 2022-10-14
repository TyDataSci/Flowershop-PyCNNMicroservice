#Build flask app
FROM ubuntu:20.04
RUN apt-get update &&  apt install -y python3-pip
COPY . .
RUN rm -r /classifier
RUN pip3 install -r requirements.txt

# ENV Vars
ARG ARG_PASS
ENV DB_PASS=${ARG_PASS}

EXPOSE 5000

ENTRYPOINT [ "python3", "main.py"]
