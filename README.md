# Safe-Anti-Drunk-Driving-System-For-Motorcycles

Virtual Enviroment

Any POST request is reflected in web page

To start the server type the following command line:

```bash
gunicorn -c gunicorn_config.py wsgi:app

```

If you are using an NGINX server add this configuration:

```bash
upstream socketio_nodes {
    server 127.0.0.1:"puerto";
}
server {
    listen 80;
    server_name  127.0.0.1:"puerto";

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:"puerto";
    }

    location /socket.io {
       include proxy_params;
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_pass http://socketio_nodes/socket.io;
   }
}
```

