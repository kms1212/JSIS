FROM ubuntu:22.04

ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apt-get -y update
RUN apt-get -y --fix-missing --no-install-recommends install build-essential python-is-python3 pip mysql-client libmysqlclient-dev curl net-tools iputils-ping libmagic-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

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
