from flask import Flask, redirect, request, render_template
from Amazon_sp_api import getToken, getOauth, getToken_oauth, listCatalogItems

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():
    redirect_url = getOauth()
    return redirect(redirect_url, code=302)


@app.route('/login', methods=['POST'])
def login():
    status_code = getToken()

    if status_code == 200:
        response = listCatalogItems()
        return render_template('index.html', catalog_items=response)
    else:
        return render_template('login.html', msg=status_code)


@app.route('/oauth_redirect', methods=['GET'])
def oauth_redirect():
    spapi_oauth_code = request.args.get('spapi_oauth_code')
    state = request.args.get('state')
    selling_partner_id = request.args.get('selling_partner_id')

    status_code = getToken_oauth(spapi_oauth_code)

    if status_code == 200:
        return render_template('login.html', msg='register success')
    else:
        return render_template('login.html', msg=status_code)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
