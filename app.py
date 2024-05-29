from flask import Flask, request, render_template, redirect, url_for, flash
import os
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB limit
app.secret_key = 'supersecretkey'

# Azure Blob Storage Configuration
STORAGE_ACCOUNT_NAME = 'eduexpertsworld'
STORAGE_ACCOUNT_KEY = 'qGwaBdfAdEKwZ9Ct9TEdjv1pbOm+SEEZZIoy0z27+B0wFkzRLUHTpNFwvIyEUc/w+kPIfMoBpCXG+AStqYm4Tw=='  # Replace with your storage account key
CONTAINER_NAME = 'uploads'

blob_service_client = BlobServiceClient(
    account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
    credential=STORAGE_ACCOUNT_KEY
)


def log_user_details(name, email, phone, country_code, due_date, filename):
    with open('logs/users.log', 'a') as log_file:
        log_file.write(
            f"Name: {name}, Email: {email}, Phone: {country_code}{phone}, Due Date: {due_date}, File: {filename}\n")


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
                blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=filename)
                blob_client.upload_blob(file, overwrite=True)
                log_user_details(name, email, phone, country_code, due_date, filename)

            flash('File uploaded successfully!', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            print(f"An error occurred: {e}")
            flash('An error occurred during file upload. Please try again.', 'danger')
            return redirect(url_for('index'))

    return render_template('index.html')


if __name__ == '__main__':
    if not os.path.exists('logs'):
        os.makedirs('logs')
    app.run(debug=True)
