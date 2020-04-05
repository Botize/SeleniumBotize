import os
import json
import sys

import time

import db_class

from os import path

print("""
Welcome to BotizeSelenium!

This is an application for running Python snippets from Botize inside Selenium.

This 'install' program will help you configure your Selenium environment

Let's get starter!
""");

if (not path.exists('chromedriver')):
	print("1. 'ChromeDriver' not found.\n\n'ChromeDriver' is a separate executable that Selenium WebDriver uses to control Chrome. Make sure you have downloaded it from https://sites.google.com/a/chromium.org/chromedriver/downloads and saved into BotizeSelenium folder.")
	sys.exit()
else:
	print("1. 'ChromeDriver' was found")

print("""
2. For communication with Botize this application requires that you have a database.

Please enter the access data to your database.
""")
  
db_host = input("Enter Database Host: ")
db_user = input("Enter Database User: ")
db_password = input("Enter Database Password: ")

print("\nNow enter the name of an existing or new database to use with this application\n")

db_name = input("Name (default 'selenium_botize'): ") or 'selenium_botize'

print("\n3. This app will check your database every 5 seconds to search for new jobs to execute.\n")

number_of_seconds_between_job_updates = input("Enter the number of seconds waiting between job updates (default 5): ") or 5

config = {
	"db_host":db_host,
	"db_user":db_user,
	"db_password":db_password,
	"db_name":db_name,
	"number_of_seconds_between_job_updates" : number_of_seconds_between_job_updates
}

try:

	db= db_class.db(config)
	db.start()
	
	with open('config.json', 'w') as outfile:
		json.dump(config, outfile)
	    
	print("Installation completed successfully.")

except:
    
    print("Installation failed.")
    