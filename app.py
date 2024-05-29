from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'


def log_user_details(name, email, phone, country_code, due_date, filename):
    with open('logs/users.log', 'a') as log_file:
        log_file.write(
            f"Name: {name}, Email: {email}, Phone: {country_code}{phone}, Due Date: {due_date}, File: {filename}\n")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        country_code = request.form['country_code']
        due_date = request.form['due_date']
        file = request.files['file']

        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            log_user_details(name, email, phone, country_code, due_date, filename)

        return redirect(url_for('index'))

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
