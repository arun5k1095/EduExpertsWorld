from flask import Flask, request, render_template, redirect, url_for, flash
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB limit
app.secret_key = 'supersecretkey'

def log_user_details(name, email, phone, country_code, due_date, filename):
    with open('logs/users.log', 'a') as log_file:
        log_file.write(f"Name: {name}, Email: {email}, Phone: {country_code}{phone}, Due Date: {due_date}, File: {filename}\n")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            country_code = request.form['country_code']
            due_date = request.form['due_date']
            file = request.files['file']
            
            if file:
                filename = file.filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                log_user_details(name, email, phone, country_code, due_date, filename)
            
            flash('File uploaded successfully!', 'success')
            return redirect(url_for('index'))
        
        except Exception as e:
            print(f"An error occurred: {e}")
            flash('An error occurred during file upload. Please try again.', 'danger')
            return redirect(url_for('index'))
    
    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    if not os.path.exists('logs'):
        os.makedirs('logs')
    app.run(debug=True)
