from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy user credentials (in real-world applications, use a database)
users = {
    "user@example.com": "password123",
    "1234567890": "mypassword"
}

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username] == password:
            return redirect(url_for('success'))
        else:
            error = "Invalid email/phone number or password."
    
    return render_template('login.html', error=error)

@app.route('/success')
def success():
    return "<h2>Login Successful</h2><p>You have logged in successfully!</p>"

if __name__ == '__main__':
    app.run(debug=True)
