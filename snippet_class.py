import json

class snippet:

    def __init__(self,driver):

        self.safe_list = ['acos', 'asin', 'atan', 'atan2', 'ceil', 'cos']
        #use the list to filter the local namespace
        self.safe_dict = dict([ (k, locals().get(k, None)) for k in self.safe_list ])
        #add any needed builtins back in.

        self.safe_dict['driver'] = driver
        #self.safe_dict['time'] = time
        self.safe_dict["save_data"] = self.save_data
        self.safe_dict["json"] = json
        context={"x":1,"y":2}
        self.safe_dict["context"] = context
        

    def run(self,snippet,input_data):
        
        try:
            if input_data!="":
                self.safe_dict["event"] = json.loads(input_data)
            else:
                self.safe_dict["event"]={"vacio":True}

            snippet=snippet+"\nresponse=handler(event,context)\nsave_data(response)"
            exec(snippet,self.safe_dict)
            print("end!")
            return {
                "meta":{
                    "code":200
                },
                "output_data":self.output_data
            }
            return self.response(200)
        except Exception as e:
            print("Error running snippet: {}".format(e))
            return self.response(210,str(e))
    
    def save_data(self,data):
        
        try:
            self.output_data=json.dumps(data)
        except ValueError as e:
            raise Exception("Data can not be saved. Not a valid dict: {}".format(data))
            print("Not a valid JSON: {}".format(data))
            return False

    def response(self,code,error_message=''):
        return {
            "meta": {
                "code":code,
                "error_message":error_message
            }
        }