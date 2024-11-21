
Bible Lamb Flask App
Overview
Bible Lamb is a Flask-based web application that integrates with the Google Gemini API to provide generative AI-powered features. This app is designed for simplicity and scalability, offering a solid foundation for future enhancements.

Features
Flask Framework: Lightweight and scalable backend development.
Google Generative AI Integration: Powered by the Gemini API.
Secure Session Management: Environment variables for enhanced security.
SQLite Database: Optional lightweight storage.

Setup Instructions


1. Clone the Repository
bash
Copy code
git clone https://github.com/anabirnbaum/biblelamb.git
cd biblelamb

2. Install Dependencies
Ensure Python (3.7 or higher) is installed. Then create a virtual environment and install the dependencies:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


3. Set Up Environment Variables
Create a .env file for local development:

plaintext
Copy code
api_key=your-google-gemini-api-key
SECRET_KEY=your-secret-key
For production, set these variables in your hosting environment.

4. Run the App Locally
Start the Flask development server:

bash
Copy code
flask run
Visit the app at http://127.0.0.1:5000/.

Deployment
To Deploy on PythonAnywhere:

Upload the project files (except .env) to PythonAnywhere.
Set environment variables (api_key and SECRET_KEY) in the PythonAnywhere web interface.
Configure the WSGI file as described in their setup guide.
Reload the web app.


File Structure
plaintext
Copy code
bible-lamb/
├── app.py             # Main Flask application
├── requirements.txt   # Python dependencies
├── .env               # Environment variables (not included in deployment)
├── templates/         # HTML files for rendering views
├── static/            # CSS, JavaScript, and images
├── README.md          # Project documentation
Environment Variables
The app requires the following environment variables:

api_key: Google Gemini API key.
SECRET_KEY: Used for Flask session management.
Dependencies
Key dependencies listed in requirements.txt:

Flask
python-dotenv
google-generativeai
SQLite (built-in with Python)
Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a feature branch:
bash
Copy code
git checkout -b feature-name
Commit your changes:
bash
Copy code
git commit -m "Add feature"
Push to the branch:
bash
Copy code
git push origin feature-name
Open a pull request.
License
This project is licensed under the MIT License.

Contact
For questions or support:

Name: Ana Birnbaum
Email: anabirnbaumlinguistics@gmail.com
GitHub: anabirnbaum

# biblelamb
 Bible Lamb is a Flask-based web application that integrates with the Google Gemini API to provide generative AI-powered features. This app is designed for simplicity and scalability, offering a foundation for future enhancements.


