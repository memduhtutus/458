from flask import Flask, render_template, request, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os
from flask_session import Session  

app = Flask(__name__)

# ✅ Secure session configuration
app.secret_key = "your-strong-secret-key"  # Replace with a strong, random key
app.config["SESSION_TYPE"] = "filesystem"  
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_KEY_PREFIX"] = "oauth_"
Session(app)  

# ✅ Initialize OAuth
oauth = OAuth(app)

# ✅ Google OAuth Configuration (Fixed)
app.config['GOOGLE_CLIENT_ID'] = "395889624025-auvbub026chb33h5sqmooi3plmmpcs9o.apps.googleusercontent.com"
app.config['GOOGLE_CLIENT_SECRET'] = "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"
google = oauth.register(
    name='google',  
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={'scope': 'openid email profile'},
    userinfo_endpoint="https://www.googleapis.com/oauth2/v3/userinfo"
)

# ✅ Dummy user credentials (for manual login)
users = {
    "user@example.com": "password123",
    "1234567890": "mypassword"
}

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handles manual login with email/password"""
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['user'] = {"email": username}  # Store user info
            return redirect(url_for('success'))
        else:
            error = "Invalid email/phone number or password."
    
    return render_template('login.html', error=error)

@app.route('/login/google')
def login_google():
    """Redirect user to Google for authentication"""
    return google.authorize_redirect(url_for('google_auth', _external=True))

@app.route('/auth/google')
def google_auth():
    """Handles Google OAuth callback"""
    token = google.authorize_access_token()
    user_info = google.get('https://www.googleapis.com/oauth2/v3/userinfo').json()
    session['user'] = user_info  # Store user info in session
    return redirect(url_for('success'))

@app.route('/success')
def success():
    """Displays success message after login"""
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    return f"<h2>Login Successful</h2><p>Welcome, {user.get('email', 'Guest')}!</p>"

@app.route('/logout')
def logout():
    """Logs out user"""
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
