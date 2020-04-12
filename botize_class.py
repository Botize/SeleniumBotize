import json
import requests

# Botize run tasks

class botize:

    def resume(self,account,task_id,mb_run_id,output_data):

        payload = {
            "account" : account,
            "task_id" : task_id,
            "mb_run_id" : mb_run_id,
            "output_data" : output_data
        }

        body_json = json.dumps(payload, default=lambda o: '<not serializable>')
        
        headers = {"Content-type": "application/json"}

        response = requests.post("https://botize.com/v1/tasks_resume", data=body_json, headers=headers)

        results = json.loads(response.text)
