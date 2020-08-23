import json

import requests
import base64

QUESTION_ID = ""
CODE = '''
'''
QUESTION_LANGUAGE = 71

API_URL = 'https://api1.knockouts.dscvit.com/api1/run'
# GET ALL TESTCASES
TESTCASE_GET_URL = "https://api1.knockouts.dscvit.com/api/admin/testcase/get/" + QUESTION_ID + "/"
headers = {
    'authorization': 'Token 1e1eddd453cf9b20ded1be69adb2aa281996c657',
    'content-type': 'application/json'
}
testcase_response = requests.request("GET", TESTCASE_GET_URL, headers=headers)
if testcase_response.status_code != 200:
    print("error")
    print(testcase_response.status_code)
    exit()
testcase_response = testcase_response.json()


def dobase64encode(tobeencoded):
    if tobeencoded is None:
        return 'null'
    else:
        return base64.b64encode(tobeencoded.encode("ascii")).decode("ascii")


def generatedicti(language_id, current_code, stdin, stdout):
    return {
        "language_id": language_id,
        "source_code": current_code,
        "stdin": dobase64encode(stdin),
        "expected_output": dobase64encode(stdout)
    }


total_count = len(testcase_response)
current_count = 0
CODE = base64.b64encode(json.dumps(CODE).encode("ascii")).decode("ascii")
for i in testcase_response:
    print("Expected STDIN,STDOUT :", i['stdin'], i['stdout'])
    payload = generatedicti(QUESTION_LANGUAGE, CODE, i['stdin'], i['stdout'])
    # print(payload)
    response = requests.request("POST", API_URL, headers=headers, json=payload)
    response = response.json()
    if response["status"]["id"] == 3:
        current_count += 1
        print("Success :", response["status"]["description"])
    else:
        print("Error :", response["status"]["description"])

if total_count == current_count:
    print("All passed!")
else:
    print("Please reupload question with proper testcases!")
