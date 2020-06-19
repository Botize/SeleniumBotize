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
import botize_class
import job_class

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

	if config["chrome_profile_path"]!="":
		# Uses a Chrome Profile
		options = webdriver.ChromeOptions() 
		options.add_argument("user-data-dir={}".format(config["chrome_profile_path"])) #Path to your chrome profile
		driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
		#print("Profile: {}".format(config["chrome_profile_path"]))
	else:
		# Without Chrome Profile
		driver = webdriver.Chrome(chromedriver_path)

	
	data = {
		"url" : driver.command_executor._url ,
		"session_id" : driver.session_id
	}

	with open('browser_session.json', 'w') as outfile:
		json.dump(data, outfile)

snippet = snippet_class.snippet(driver)
botize = botize_class.botize()
job = job_class.job()

loop = True

# Add fake job
#db.add_job("print(5+1)")

print ("Browser Ready! Waiting for jobs.\n")

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

		job_item = job.make_job(response["job"])

		print("[JOB ID{}:@{}:#{}]".format(job_item['id'],job_item['account'],job_item['task_id']))

		db.remove_job(job_item['id'])

		response = snippet.run(job_item["snippet"],job_item["input_data"],context)

		if response["meta"]["code"]!=200:
			payload= {
				"code":response["meta"]["code"],
				"error_message":response["meta"]["error_message"],
				"account":job_item["account"],
				"task_id":job_item["task_id"],
				"snippet":job_item["snippet"],
				"output_data":""
			}
		else:
			payload= {
				"code":response["meta"]["code"],
				"error_message":'',
				"account":job_item["account"],
				"task_id":job_item["task_id"],
				"snippet":job_item["snippet"],
				"output_data":response.get("output_data")
			}

			botize.resume(job_item["account"],job_item["task_id"],job_item["input_data"]["mb_run_id"],response.get("output_data"),response.get("data_to_save"))
			

		db.add_output(payload)

		# db.remove_job(job_item['id'])

		print("Waiting for next job...")
		
	time.sleep(config['number_of_seconds_between_job_updates'])