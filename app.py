import selenium
import pathlib
import os
import json
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os import path

import db_class
import snippet_class

# Init
context={}

# Check 'chromedriver'
chromedriver_path = os.getcwd()+'/chromedriver'
	
if (not path.exists(chromedriver_path)):
	print("Error: 'ChromeDriver' not found.\n\n'ChromeDriver' is a separate executable that Selenium WebDriver uses to control Chrome. Make sure you have downloaded it from https://sites.google.com/a/chromium.org/chromedriver/downloads and saved into BotizeSelenium folder.")
	sys.exit()

# Open configuration
with open('config.json', 'r') as json_file:
	config = json.load(json_file)
	
# Connect to database
db= db_class.db(config)
db.start()

# Open a new browser or reuse current browser
try:

	# Reuse current Browser
	with open('browser_session.json', 'r') as json_file:
		data = json.load(json_file)

	url = data["url"]
	session_id = data["session_id"]
	
	driver = webdriver.Remote(command_executor=url,desired_capabilities={})
	driver.close() # Close dummy browser
	
	driver.session_id = session_id

	context["browser_title"] = driver.title
	context["browser_url"] = driver.current_url

except:
	
	# Open a new Browser
	driver = webdriver.Chrome(chromedriver_path)
	
	data = {
		"url" : driver.command_executor._url ,
		"session_id" : driver.session_id
	}

	with open('browser_session.json', 'w') as outfile:
		json.dump(data, outfile)

snippet = snippet_class.snippet(driver)

loop = True

# Add fake job
#db.add_job("print(5+1)")

print ("Botize Selenium running.")

while loop:

	response = db.get_next_job()

	if response["meta"]["code"]!=200:
		payload= {
			"code":response["meta"]["code"],
			"error_message":response["meta"]["error_message"],
			"snippet":"",
			"output_data":""
		}

		db.add_output(payload)
	
	if "job" in response:

		job = response["job"]

		print("Running job...")

		response = snippet.run(job["snippet"],job["input_data"],context)

		if response["meta"]["code"]!=200:
			payload= {
				"code":response["meta"]["code"],
				"error_message":response["meta"]["error_message"],
				"snippet":job["snippet"],
				"output_data":""
			}
		else:
			payload= {
				"code":response["meta"]["code"],
				"error_message":'',
				"snippet":job["snippet"],
				"output_data":response.get("output_data")
			}

		db.add_output(payload)

		db.remove_job(job['id'])
		
	time.sleep(config['number_of_seconds_between_job_updates'])