# Note that this file is not being used in the docker-compose file
# at the moment, but I decided to let it here to show that, in there
# future, I could extend airflow image and install any aditional
# package I might need. In this case I would have to update the
# docker-compose file to build from this Dockerfile instead of using
# directly airflow:2.4.2.
FROM apache/airflow:2.4.2
COPY requirements.txt /requirements.txt
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /requirements.txt