import sys, os, base64, datetime, hashlib, hmac 

HOST = 'sellingpartnerapi-na.amazon.com'
SERVICE = 'execute-api'
REGION = 'us-east-1'
ALGORITHM = 'AWS4-HMAC-SHA256'
signed_headers = 'host;x-amz-date'

def parseParameter(parameters):
    querystring = ''
    for key, val in parameters.items():
        querystring += f'{key}={val}&'
    
    return querystring[:-1]

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')

    return kSigning

def authorization(method, canonical_uri, request_parameters, access_key, secret_key):
    t = datetime.datetime.utcnow()
    amzdate = t.strftime('%Y%m%dT%H%M%SZ')
    datestamp = t.strftime('%Y%m%d') 

    canonical_querystring = parseParameter(request_parameters)
    canonical_headers = 'host:' + HOST + '\n' + 'x-amz-date:' + amzdate + '\n'
    payload_hash = hashlib.sha256(('').encode('utf-8')).hexdigest()
    
    canonical_request = f"{method}\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{payload_hash}"
    credential_scope = f"{datestamp}/{REGION}/{SERVICE}/aws4_request"

    request_hash = hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
    string_to_sign = f"{ALGORITHM}\n{amzdate}\n{credential_scope}\n{request_hash}"

    signing_key = getSignatureKey(secret_key, datestamp, REGION, SERVICE)
    signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

    authorization_header = f"{ALGORITHM} Credential={access_key}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}"

    return amzdate, authorization_header