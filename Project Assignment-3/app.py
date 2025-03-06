from flask import Flask, redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = "your_secret_key"

oauth = OAuth(app)

# Google OAuth Configuration
google = oauth.register(
    name='google',
    client_id='YOUR_GOOGLE_CLIENT_ID',
    client_secret='YOUR_GOOGLE_CLIENT_SECRET',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params={'scope': 'email profile'},
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    client_kwargs={'scope': 'openid email profile'},
)

# Facebook OAuth Configuration
facebook = oauth.register(
    name='facebook',
    client_id='YOUR_FACEBOOK_CLIENT_ID',
    client_secret='YOUR_FACEBOOK_CLIENT_SECRET',
    authorize_url='https://www.facebook.com/dialog/oauth',
    authorize_params={'scope': 'email'},
    access_token_url='https://graph.facebook.com/oauth/access_token',
    access_token_params=None,
    client_kwargs={'scope': 'email'},
)

@app.route('/')
def home():
    return "<h1>Welcome to Flask OAuth2 Authentication</h1><a href='/login/google'>Login with Google</a> | <a href='/login/facebook'>Login with Facebook</a>"

@app.route('/login/<provider>')
def login(provider):
    if provider == 'google':
        return google.authorize_redirect(url_for('authorize', provider='google', _external=True))
    elif provider == 'facebook':
        return facebook.authorize_redirect(url_for('authorize', provider='facebook', _external=True))
    return "Invalid provider", 400

@app.route('/authorize/<provider>')
def authorize(provider):
    if provider == 'google':
        token = google.authorize_access_token()
        user_info = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
    elif provider == 'facebook':
        token = facebook.authorize_access_token()
        user_info = facebook.get('https://graph.facebook.com/me?fields=id,name,email').json()
    else:
        return "Invalid provider", 400

    session['user'] = user_info
    return jsonify(user_info)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
