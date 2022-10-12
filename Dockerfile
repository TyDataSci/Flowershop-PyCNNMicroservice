#Build flask app
FROM python:3.7
COPY . .
RUN pip install -r requirements.txt
# ENV Vars
ARG ARG_PASS
ENV DB_PASS=${ARG_PASS}

EXPOSE 5000

ENTRYPOINT [ "python", "./main.py"]
