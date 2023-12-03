# Topics-of-Software

Installing Instruction:

1. Download and install Node.js
	https://nodejs.org/en/download/
	after install, check
	```
	node -v
	npm -v
	```
   
2. Navigate to auction-frontend
	```
	cd .\auction-frontend\
	npm install
	```

3. Setting Up a Virtual Environment (Optional)
	```
	python -m venv venv
	venv\Scripts\activate
	```

  	trouble shooting: if you see message like this
   	![image](https://github.com/liangjunchen88/Topics-of-Software/assets/113968753/0577d90b-d135-4dc9-aaf0-3ec70d937eb6)
   
	```
    	Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
	```


5. Install Dependencies
	```
	pip3 install -r requirements.txt
 	// if pip3 doesn't work for you, try pip
 	pip install -r requirements.txt
	```

6. Open MySQL Shell
	```
	mysqlsh
	```

7. Enter SQL Mode
	```
	\sql
	```
   
8. Connect to Your Local Admin Account
	```
	\connect root@localhost
	```

9. Create and Set Up the New Database
	```
	DROP DATABASE javaSavesUs;
	CREATE DATABASE javaSavesUs;
	USE javaSavesUs;
	source ./database/javaSavesUs_db.sql;
	```

10. Create a .env File using IDE
	
 	Open your code editor or IDE (like Visual Studio Code, PyCharm, etc.).

	Navigate to each MircroService folder.

	Create a new file at the root of this folder and name it .env.

11. Add Database Connection Details
	
 	In the .env file, you will add the lines provided, replacing placeholders with your actual database information. 
	```
	340DBHOST=localhost
	340DBUSER=root
	340DBPW=your_mysql_password
	340DB=javaSavesUs
	```

 	Should be like this after step9 and step10
	![image](https://github.com/liangjunchen88/Topics-of-Software/assets/113968753/23b72210-7868-4fcb-8640-2f315ab69bc9)


12. Running the Application

	With the database set up and the .env file configured, your application should now be able to connect to your database.
	
	1. Open Your Terminal in code editor/IDE
	
	2. Activate Your Virtual Environment (If You Used One)
	
	3. Run the Application
	split into 5 terminals
	```
	python .\MicroServices\alert-service\app_alert.py
	python .\MicroServices\auction-service\app_auction.py
	cd .\MicroServices\item-service\
	python app_item.py
	python .\MicroServices\log-service\app_log.py
	python .\MicroServices\notification-service\app_notification.py
	python .\MicroServices\user-service\app_user.py

	cd .\auction-frontend\
	npm start
	```

 	4. Access the Web Application

      	Open your web browser and go to http://127.0.0.1:9112/.
     
     	This is the local address where your Flask app is running.
     
	Flask will also output the URL in the terminal, confirming where the app is active.

 	Trouble Shooting:
	
	if you meet the any issue with the depencies like this:
	![image](https://github.com/liangjunchen88/Topics-of-Software/assets/113968753/738615bb-075f-4a6c-bd25-44bfdf296c52)

	You need to manual pip install the dependencies you need, here I provide all the command you may need.
	
	```
 	pip install flask
 	pip install mysqlclient
	pip install python-dotenv
	pip install flask-cors
	pip install pymysql
 	```

If you have father qs, plz reach out anytime on our team chat group ^_^

-------------------------------------------------------------------------

Process of creating new branch

1. Web App
   
	Code -> Main -> View all branches -> New branch


2. Terminal
   
	git fetch

	git checkout [branchName]
	
	make changes...

	git add .

	git commit -m "...."

	git push


3. Pull Request
   
	-> New pull request
