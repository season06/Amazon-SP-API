# Amazon-sp-api

## Environment
- Ubuntu 20.04.1
- Python 3.8

## Create AWS credentials
```bash
touch ~/.aws/credentials
```
- should include following information in `credentials` file
```
[default]
aws_access_key_id = XXXXXXXXXXXXXXXXXXXX 
aws_secret_access_key = YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
```

## Set Virtual Environment
``` bash
cd ~
pip install virtualenv
virtualenv venv
source ~/venv/bin/activate
```

## mod_wsgi
``` bash
apt-get install apache2
apt-get install libapache2-mod-wsgi-py3
```

## Set Apache conf
``` bash
cd /etc/apache2/sites-available/
touch Amazon-sp-api.conf
```
```
WSGIPythonPath /home/season/venv/lib/python3.8/site-packages

<VirtualHost *:80>
    ServerName season.coder.tw

    WSGIDaemonProcess Amazon-sp-api threads=5
    WSGIScriptAlias / /var/www/html/Amazon-sp-api/app.wsgi

    <Directory /var/www/html/Amazon-sp-api>
        WSGIProcessGroup Amazon-sp-api
        WSGIApplicationGroup %{GLOBAL}
        WSGIScriptReloading On
        Order deny,allow
        Allow from all
    </Directory>
</VirtualHost>
```
``` bash
a2ensite Amazon-sp-api.conf
service apache2 reload
```

## Build the Environment
```bash
cd Amazon-sp-api
pip install -r requirements.txt
export FLASK_APP=app.py
python -m flask run
```