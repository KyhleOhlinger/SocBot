#!/usr/bin/python3
import requests
import json

#curl -XPOST -H 'Authorization: Bearer OkfpdlSk6HSjrnHbuQpF22X8Aiq8IBT8' -H 'Content-Type: application/json' http://127.0.0.1:9000/api/case -d '{"title": "My first case","description": "This case has been created by my custom script"}'


class CaseInstances:  
    endpoint = None
    headers = None

    def create_case(self,prepared_data):
        """
        Prepared data should be json which includes at least `message_url`
        """       
        message_url = self.endpoint + 'api/case'
        return requests.post(message_url, data=prepared_data, headers=self.headers)

    def get_case(self): 
        message_url = self.endpoint + 'api/case'
        return requests.get(message_url,headers=self.headers)

    def delete_case(self,caseId):
        message_url = self.endpoint + f'api/case/{caseId}'
        return requests.delete(message_url,headers=self.headers)
    
    def update_case(self,prepared_data,caseId):
        message_url = self.endpoint + f'api/case/{caseId}'
        return requests.patch(message_url,data=prepared_data,headers=self.headers)
    

class CaseManagement(CaseInstances):  
    endpoint = "http://192.168.50.3:9000/"
    headers = {"Authorization": "Bearer uKJfY6Zse2yRDZWboDgDvc7jYIXZ0Si+"}

    def __init__(self, *args, **kwargs):
        super(CaseInstances, self).__init__()

    def create_cases(self):
        case_data = {
          'title': 'My Second Python Case',
          'description': 'This case has been created by my custom Python Script, again'
        }
        case = self.create_case(case_data).json()
        print("=================== New Case ===================")
        print(case)
      
    def get_cases(self):
        active_case = self.get_case().json()
        print("=================== Open Cases ===================")
        for case in active_case:
            if(case['status'] == "Open"):
              print("Owner:\t" + str(case['owner']))
              print("Title:\t" + str(case['title']))
              print("Identifier:\t" + str(case['id']) + "\n")
              print(case)

          
    def delete_cases(self,caseId):
        deleted_case = self.delete_case(caseId)
        print(f"\n=================== Deleted Case {caseId} ===================\n")
      
    def update_cases(self,caseId):
        case_data = {
          'tlp': 3
        }
        updated_case = self.update_case(case_data, caseId).json()
        print(f"\n=================== Updated Case {caseId} ===================\n")
        print(updated_case)


if __name__ == '__main__':  
    case = CaseManagement()
    #case.post_handler()
    case.get_cases()
    #case.delete_cases("AXPIxdp7CjxhYhH1HK21")
    #case.update_cases("AXPIzVlICjxhYhH1HK28")
