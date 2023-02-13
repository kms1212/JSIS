FROM nginx

# Create workdir
RUN mkdir /usr/local/workdir
WORKDIR /usr/local/workdir

# Copy project files
COPY webapp/dist /var/www/html

# Set permissions
RUN chmod -R 755 /var/www/html

# Copy configuration files
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080
