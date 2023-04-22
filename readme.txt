Steps to run website:

	0. Make sure you have Python installed (latest version preferable)
	
	Then, open a command prompt and navigate to the "soen-final-project/" repo
	
	1. create virual Python environment
	
		$ python3 -m venv venv
	
	to Activate environment (must be aactive when running webapp) type command:
		
		$ venv\Scripts\activate
	
	2. Install Flask:
	
		$ pip install flask
		
	3. Install WTForms
	
		$ pip install flask-wtf
	
	4. Install email validator
	
		$ pip install email_validator
	
	5. Install SQL Alchemy
	
		$ pip install flask-sqlalchemy
		
	6. Install Login manager
	
		$ pip install flask-login
	
	7. Install Pillow for images
	
		$ pip install Pillow
	
	Run website with command (make sure virtual env is activated):
	
	$ venv\Scripts\activate		// if virtual env not already activated
	$ python run.py				// run the app
	
	Visit website by opening your favorite web browser typing the following URL:
	
	http://localhost:5000 or http://127.0.0.1:5000
	
	
	Misc:
	
	For creating database (from flask shell):
	
	$ set FLASK_APP=run.py		// set flask app env variable to app (run.py)
	$ set FLASK_DEBUG=1		// launch in debug mode
	
	$ flask shell			// enter the shell
	$ db.create_all() 		// create tables from models
	$ db.drop_all()			// clear all tables
	
	
