Steps to run website:

	0. Make sure python is installed
	
	1. create virual Python environment
	
		$ mkdir myproject
		$ cd myproject
		$ python3 -m venv venv
	
		Activate environment
		
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
	
	For creating database (from flask shell):
	
	$ set FLASK_APP=run.py	// set flask app env variable to app (run.py)
	$ flask shell			// enter the shell
	$ db.create_all() 		// create tables from models
	$ db.drop_all()			// clear all tables
	
	Run website with command (make sure virtual env is activated):
	
	$ venv\Scripts\activate		// if virtual env not already activated
	$ python run.py				// run the app
	
	Visit website by opening your favorite web browser typing the following URL:
	
	http://localhost:5000 or http://127.0.0.1:5000
	
