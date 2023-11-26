# Topics-of-Software

Installing Instruction:

1. Clone to your local
   
2. Navigate to local directory
	```
	cd C:\Users\dell\auctionSite\gotham-auctions
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
	```

6. Open MySQL Shell
	```
	(venv) PS C:\Users\dell\auctionSite\gotham-auctions> mysqlsh
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
	CREATE DATABASE gotham;
	USE gotham;
	source ./database/gotham_db.sql;
	```

10. Create a .env File using IDE
	
 	Open your code editor or IDE (like Visual Studio Code, PyCharm, etc.).

	Navigate to the gotham-auctions project folder.

	Create a new file at the root of this folder and name it .env.

11. Add Database Connection Details
	
 	In the .env file, you will add the lines provided, replacing placeholders with your actual database information. 
	```
	340DBHOST=localhost
	340DBUSER=root
	340DBPW=your_mysql_password
	340DB=gotham
	```

 	Should be like this after step9 and step10
	![image](https://github.com/liangjunchen88/Topics-of-Software/assets/113968753/2abe79d1-a135-4681-a7dc-dd55bdc5f8ad)

12. Running the Application

	With the database set up and the .env file configured, your application should now be able to connect to your database.
	
	1. Open Your Terminal in code editor/IDE
	
	2. Activate Your Virtual Environment (If You Used One)
	
	3. Run the Application
	```
	python3 app.py
	```

 	4. Access the Web Application

      	Open your web browser and go to http://127.0.0.1:9112/.
     	This is the local address where your Flask app is running.
	Flask will also output the URL in the terminal, confirming where the app is active.
    

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
