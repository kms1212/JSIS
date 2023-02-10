FROM ubuntu:22.04

ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y --fix-missing install build-essential python-is-python3 pip mysql-client libmysqlclient-dev curl net-tools iputils-ping libmagic-dev nginx

# Create workdir
RUN mkdir /usr/local/workdir
WORKDIR /usr/local/workdir

# Install python dependencies
COPY image-assets/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY jsis ./api
COPY webapp/dist /var/www/html

# Set permissions
RUN chmod -R 755 /var/www/html

# Copy configuration files
COPY image-assets/nginx.conf /etc/nginx/sites-available/default

# Copy init script
COPY image-assets/init-server.sh .

EXPOSE 8000
CMD ["bash", "-c", ". ./init-server.sh"]
