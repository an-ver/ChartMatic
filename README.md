# ChartMatic - App Description

    ChartMatic is a web application developed using the Flask framework. It parses data from Kaggle and the International Monetary Fund (IMF) to generate various charts for different countries, focusing on environmental and demographic indicators. Users can create bar, scatter, or line charts, each offering unique features and insights.

## Files included
    
    - charts: Contains scripts responsible for generating individual charts.
    - csv: Includes the initial CSV files, a Python script for data modification, and the modified CSV files.
    - DB_Backup: Backup of the application database.
    - Include/Lib/Scripts: Auto-generated files containing essential libraries and features.
    - images: Stores the photos of the charts, which are parsed by app.py.
    - templates: Contains home.html, the front page of the application.
    - app.py: The main application file responsible for connecting all components.

## Purpose

    The primary purpose of ChartMatic is to simplify the workflow of analysts by generating comprehensive plots. With ChartMatic, analysts can easily view various plots for selected countries and indicators, facilitating data analysis and helping them draw meaningful conclusions. By utilizing ChartMatic, analysts can focus on interpreting data rather than spending time on chart creation, thereby enhancing productivity and decision-making processes.

## Setup the environment
    
-	Download the project’s zip file.

-	Create a FlaskApps file, open the FlaskApps file and unzip it there (FlaskApps/ChartMatic-main).
-	Install from the command line the follows:
    -	python -m venv ChartMatic
	-  .\ChartMatic\Scripts\activate
    -  Go to View/Command Pallette/ Python Select Interpreter
    - Enter Interpreter path
    - Select find and select ChartMatic/Scripts/pyhton.exe

    - Go back to command line and write :
    - python -m pip install --upgrade pip

    - python -m pip install flask

    - python -m pip install matplotlib

    - python -m pip install sqlalchemy

    - python -m pip install pandas

    - python -m pip install flask_mysqldb

    - python -m pip install pymysql

-	Copy the files : csv, charts, templates, app.py, DB_Backup from the zip file to your NEW Chartmatic file.
 
-	Write python app.py in the command line .
-	Server : localhost:5.000

    **Note that you need to adjust you db configuration settings that match your db. You are free to download our db backup that contains the tables. Create your own db and import our tables. Adjust home.html and the charts scripts with your own configuration settings. **

## Run commands

    To run the application locally, use the following commands:
    
    -python app.py
    -Go to localhost:5.000

## Our team

    Anastasia Varoucha - 4288
    Katerina Papaxristopoulou - 4148