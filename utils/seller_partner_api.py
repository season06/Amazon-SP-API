import requests, configparser, json, os, base64
from datetime import datetime, timedelta
import boto3
import urllib.parse

from signature import authorization

config_path = '/var/www/html/Amazon-SP-API/config.ini'
config = configparser.RawConfigParser()

ENDPOINT = 'https://sellingpartnerapi-na.amazon.com'
HOST = 'sellingpartnerapi-na.amazon.com'

HEADERS = {
    'host': HOST,
    'x-amz-access-token': '',
    'x-amz-security-token': '',
    'x-amz-date': '', 
    'Authorization': ''
}

random = os.urandom(256)

def getOauth():
    config.read(config_path)

    request_url = 'https://sellercentral.amazon.com/apps/authorize/consent'
    parameters = {
        'application_id': config.get('INFO', 'application_id'),
        'state': base64.b64encode(random),
        'version': 'beta' # test version
    }

    r = requests.get(request_url, params=parameters)
    if r.status_code == 200:
        return r.history[-1].url
    else:
        print(r.status_code)
        print(r.text)
        return '/'


def getToken_oauth(code):
    config.read(config_path)

    request_url = 'https://api.amazon.com/auth/o2/token'
    parameters = {
        'grant_type': 'authorization_code',
        'code': code, #ANGLDagVzDQXozWcAtTR,  # spapi_oauth_code
        'redirect_uri': urllib.parse.quote_plus(config.get('INFO', 'redirect_uri')),
        'client_id': config.get('INFO', 'client_id'),
        'client_secret': config.get('INFO', 'client_secret')
    }
    header = {
        'content_type': 'application/x-www-form-urlencoded;charset=utf-8'
    }

    r = requests.post(request_url, data=parameters, headers=header)
    response = json.loads(r.text)

    if r.status_code == 200:
        config.set('TOKEN', 'access_token', response['access_token'])
        config.set('TOKEN', 'refresh_token', response['refresh_token'])
        config.set('TIME', 'expired_time', response['expires_in'])
        with open(config_path, 'w') as configfile:
            config.write(configfile)
    else:
        print(r.status_code)
        print(r.text)

    return r.status_code


def getToken():
    config.read(config_path)

    request_url = 'https://api.amazon.com/auth/o2/token'
    parameters = {
        'grant_type': 'refresh_token',
        'client_id': config.get('INFO', 'client_id'),
        'client_secret': config.get('INFO', 'client_secret'),
        'refresh_token': config.get('TOKEN', 'refresh_token'),
    }
    header = {
        'content_type': 'application/x-www-form-urlencoded'
    }
    request_parameters = json.dumps(parameters)
    r = requests.post(request_url, data=request_parameters, headers=header)
    response = json.loads(r.text)
    expired_time = (datetime.now() + timedelta(seconds = response['expires_in'])).timestamp()

    # get AWS token
    sts_client = boto3.client('sts',
                              aws_access_key_id=config.get('AWS', 'aws_access_key_id'),
                              aws_secret_access_key=config.get('AWS', 'aws_secret_access_key'))

    response_aws = sts_client.assume_role(
        RoleArn="arn:aws:iam::762759851080:role/SP-API",
        RoleSessionName="SP-API",
        DurationSeconds=3600
    )
    credentials = response_aws['Credentials']

    if r.status_code == 200:
        config.read(config_path)
        config.set('TOKEN', 'access_token', response['access_token'])
        config.set('AWS', 'access_key', credentials['AccessKeyId'])
        config.set('AWS', 'secret_key', credentials['SecretAccessKey'])
        config.set('AWS', 'session_token', credentials['SessionToken'])
        config.set('TIME', 'expired_time', expired_time)
        with open(config_path, 'w') as configfile:
            config.write(configfile)
    else:
        print(r.status_code)
        print(r.text)

    return r.status_code

def listCatalogItems():
    method, path = 'GET', '/catalog/v0/items'
    request_url = ENDPOINT + path

    parameters = {
        'MarketplaceId': 'ATVPDKIKX0DER',
        'SellerSKU': 'VQ-8M14-QZB1',
    }
    
    HEADERS['x-amz-access-token'], HEADERS['x-amz-security-token'] = config.get('TOKEN', 'access_token'), config.get('AWS', 'session_token')
    HEADERS['x-amz-date'], HEADERS['Authorization'] = authorization(
        method, path, parameters, config.get('AWS', 'access_key'), config.get('AWS', 'secret_key'))

    r = requests.get(request_url, params=parameters, headers=HEADERS)
    if r.status_code == 200:
        return r.text
    else:
        print(r.url)
        print(r.status_code)
        print(r.text)
