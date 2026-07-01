#!/bin/bash
mkdir -p storage/logs
mkdir -p storage/framework/sessions
mkdir -p storage/framework/views
mkdir -p storage/framework/cache/data
php artisan storage:link --quiet 2>/dev/null || true
php artisan migrate --force --quiet 2>/dev/null || true
php artisan db:seed --force --quiet 2>/dev/null || true
php artisan serve --host=0.0.0.0 --port=$PORT
