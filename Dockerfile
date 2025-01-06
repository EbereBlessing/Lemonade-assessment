# Stage 1: Base image for installing dependencies
FROM php:8.2-fpm-alpine AS base

# Set working directory
WORKDIR /var/www/html

# Install system dependencies
RUN apk add --no-cache bash git curl libpng-dev oniguruma-dev libxml2-dev zip unzip && \\
    docker-php-ext-install pdo pdo_mysql mbstring exif pcntl bcmath gd

# Install Composer
COPY --from=composer:2.6 /usr/bin/composer /usr/bin/composer

# Copy application code
COPY . .

# Install Laravel dependencies
RUN composer install --no-dev --optimize-autoloader

# Set permissions
RUN chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache

# Expose port 9000 for PHP-FPM
EXPOSE 9000

# Stage 2: Production-ready image
FROM php:8.2-fpm-alpine AS production

# Set working directory
WORKDIR /var/www/html

# Copy application code from the base stage
COPY --from=base /var/www/html /var/www/html

# Set permissions
RUN chown -R www-data:www-data /var/www/html

# Expose port 9000 for PHP-FPM
EXPOSE 9000

# Run PHP-FPM as the container's default process
CMD ["php-fpm"]
