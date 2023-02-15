FROM ubuntu:22.04

ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y --fix-missing install build-essential python-is-python3 pip mysql-client libmysqlclient-dev curl net-tools iputils-ping libmagic-dev

# Create workdir
RUN mkdir /usr/local/workdir
WORKDIR /usr/local/workdir

# Install python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY src .

EXPOSE 8000
CMD ["bash", "-c", ". ./init-server.sh"]
