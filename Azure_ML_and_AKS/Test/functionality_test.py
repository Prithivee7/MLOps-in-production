import requests
import json

url = "<Enter AKS url here>"

payload = json.dumps({
  "Pclass": 1,
  "Sex": 0,
  "Age": 38,
  "SibSp": 1,
  "Parch": 0,
  "Fare": 71.2833,
  "Embarked": 2
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
response_data = json.loads(response)
if response_data['prediction'] == 1:
    print("The prediction is correct")
else:
    print("The prediction is wrong")