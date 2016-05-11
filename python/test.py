output = [u'server {', u'server_name drupal.bootdev.com;', u'root /srv/www/bootdev.com; ## <-- Your only path reference.', u'access_log /srv/www/bootdev.com/logs/access.log;', u'error_log /srv/www/bootdev.com/logs/error.log;', u'location = /favicon.ico {', u'log_not_found off;', u'access_log off;', u'}', u'location = /robots.txt {', u'allow all;', u'log_not_found off;', u'access_log off;', u'}', u'location = /backup {', u'deny all;', u'}', u'location ~* \\.(txt|log)$ {', u'deny all;', u'}', u'location ~ \\..*/.*\\.php$ {', u'return 403;', u'}', u'location / {', u'try_files $uri @rewrite;', u'index index.html;', u'}', u'location /documentation {', u'autoindex on;', u'}', u'location @rewrite {', u'rewrite ^/(.*)$ /index.php?q=$1;', u'}', u'location ~ \\.php$ {', u'fastcgi_split_path_info ^(.+\\.php)(/.+)$;', u'include fastcgi_params;', u'fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;', u'fastcgi_intercept_errors on;', u'fastcgi_pass unix:/var/run/php-fpm/php-fpm.sock;', u'fastcgi_cache off;', u'fastcgi_cache_bypass $no_cache;', u'fastcgi_no_cache $no_cache;', u'fastcgi_cache_key $cache_uid@$host$request_uri;', u'fastcgi_cache_valid 200 301 15s;', u'fastcgi_cache_valid 302     1m;', u'fastcgi_cache_valid 404     1s;', u'fastcgi_cache_min_uses 1;', u'fastcgi_cache_use_stale error timeout invalid_header updating http_500;', u'fastcgi_ignore_headers Cache-Control Expires;', u'fastcgi_pass_header Set-Cookie;', u'fastcgi_pass_header Cookie;', u'add_header X-Micro-Cache $upstream_cache_status;', u'expires epoch;', u'fastcgi_cache_lock on;', u'}', u'location ~* \\.(js|css|png|jpg|jpeg|gif|ico)$ {', u'expires max;', u'log_not_found off;', u'}', u'}']

import os, sys
lib_path = os.path.abspath(os.path.join("./nginxparser"))
sys.path.append(lib_path)
import nginxparser
 
config_value = nginxparser.loads(''.join(output))

print ''.join(output)
