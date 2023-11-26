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

4. Install Dependencies
   ```
   pip3 install -r requirements.txt
   ```

5. Open MySQL Shell
   ```
   (venv) PS C:\Users\dell\auctionSite\gotham-auctions> mysqlsh
   ```

6. Enter SQL Mode
   ```
   \sql
   ```
   
7. Connect to Your Local Admin Account
```
\connect root@localhost
```

8. Create and Set Up the New Database
	```
	CREATE DATABASE gotham;
	USE gotham;
	source ./database/gotham_db.sql;
	```

9. Create a .env File using IDE
	Open your code editor or IDE (like Visual Studio Code, PyCharm, etc.).
	Navigate to the gotham-auctions project folder.
	Create a new file at the root of this folder and name it .env.

10. Add Database Connection Details
	In the .env file, you will add the lines provided, replacing placeholders with your actual database information. 
	```
	340DBHOST=localhost
	340DBUSER=root
	340DBPW=your_mysql_password
	340DB=gotham
	```

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
