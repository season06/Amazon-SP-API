# Amazon-sp-api

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

## Build the Environment
```bash
cd Amazon-sp-api
pip install -r requirements.txt
export FLASK_APP=app.py
python -m flask run
```