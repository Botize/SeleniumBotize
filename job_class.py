import json

# Job Class

class job:

    def make_job(self,row):

        if row["input_data"]!="":
            input_data = json.loads(row["input_data"])
        else:
            input_data = {}
        
        job_item = {
            "id"      : row["id"],
            "account" : row["account"],
            "task_id" : row["task_id"],
            "snippet" : row["snippet"],
            "input_data" : input_data
        }

        return job_item
        
