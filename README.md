# Amazon Seller Partner API

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
touch Amazon-SP-API.conf
```
```
WSGIPythonPath /home/season/venv/lib/python3.8/site-packages

<VirtualHost *:80>
    ServerName season.coder.tw

    WSGIDaemonProcess Amazon-SP-API threads=5
    WSGIScriptAlias / /var/www/html/Amazon-SP-API/app.wsgi

    <Directory /var/www/html/Amazon-SP-API>
        WSGIProcessGroup Amazon-SP-API
        WSGIApplicationGroup %{GLOBAL}
        WSGIScriptReloading On
        Order deny,allow
        Allow from all
    </Directory>
</VirtualHost>
```
``` bash
a2ensite Amazon-SP-API.conf
service apache2 reload
```

## Build the Environment
```bash
cd Amazon-SP-API
pip install -r requirements.txt
export FLASK_APP=app.py
python -m flask run
```

## Reference
[selling-partner-api-docs](https://github.com/amzn/selling-partner-api-docs) <br>
[Selling Partner API Developer Guide](https://github.com/amzn/selling-partner-api-docs/blob/main/guides/developer-guide/SellingPartnerApiDeveloperGuide.md)
