# Основной конфиг для Nginx в контейнере
upstream t-los-django-1 {
    # Связь с контейнером Django через Docker network
    server django:5000;  # "django" — имя сервиса в docker-compose.yml
}

server {
    listen 80;
    server_name _;

    # Безопасность: скрываем версию Nginx
    server_tokens off;

    # Статические файлы Django
    location /static/ {
        proxy_pass http://django:5000/; #добавил для проверки
        alias /app/staticfiles/;
        expires 30d;
        access_log off;
    }

    # Медиа-файлы (если используются)
    location /media/ {
        alias /var/www/media/;
        expires 30d;
        access_log off;
    }

    # Проксирование всех остальных запросов к Gunicorn
    location / {
        proxy_pass http://django:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Для WebSocket (если нужно)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Запрет доступа к скрытым файлам (.env, .git)
    location ~ /\. {
        deny all;
    }
}