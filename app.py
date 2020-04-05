import selenium
import pathlib
import os
import json
import sys

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



import db_class
import snippet_class

with open('config.json', 'r') as json_file:
	config = json.load(json_file)
	
db= db_class.db(config)
db.start()

chromedriver = '/usr/local/bin/chromedriver'
chromedriver = os.getcwd()+'/chromedriver'

try:

	with open('browser_session.json', 'r') as json_file:
		data = json.load(json_file)

	url = data["url"]
	session_id = data["session_id"]
	
	driver = webdriver.Remote(command_executor=url,desired_capabilities={})
	driver.close() # Close dummy browser
	
	driver.session_id = session_id

	title = driver.title
	url = driver.current_url

	print(f"{title}: {url}")
	print("Reuse Browser")

except:
	
	driver = webdriver.Chrome(chromedriver)
	
	data = {
		"url" : driver.command_executor._url ,
		"session_id" : driver.session_id
	}

	with open('browser_session.json', 'w') as outfile:
		json.dump(data, outfile)
	
	print("New Browser")
	
	driver.get('https://web.whatsapp.com')

snippet = snippet_class.snippet(driver)

loop = True

# Add fake job
#db.add_job("""print(5+1)
#data_to_save=json.dumps({"x":1,"y":2})
#save_data(data_to_save)
#""")

while loop:

	print("reading...")
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

		print("running...")
		print(job)

		response = snippet.run(job["snippet"],job["input_data"])

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

		print("OUTPUT DATA:")
		print(response.get("output_data"))
		db.add_output(payload)

		print("removing...")
		db.remove_job(job['id'])

		print(payload)
		
	print("wait...")
	time.sleep(config['number_of_seconds_between_job_updates'])

"""
name = "Hermana" # Name of the user or group
msg = "este es un mensaje de prueba!"

input("Enter anithing after scanning QR Code")

user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
user.click()

time.sleep( 2 )

msg_box = driver.find_element_by_css_selector('._2S1VP.copyable-text.selectable-text')
footer = driver.find_element_by_xpath('//footer')
msg_box = footer.find_element_by_css_selector('._2S1VP.copyable-text.selectable-text')
msg_box.send_keys(msg)

time.sleep( 2 )

button = footer.find_elements_by_xpath('//button')

size = len(button)
target_element = button[size -1]

target_element.click()
"""
