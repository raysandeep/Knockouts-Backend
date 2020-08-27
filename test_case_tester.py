import json

import requests
import base64

QUESTION_ID = "e2b826fb-2607-4781-b727-9e9e5f418600"
CODE = '''
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0
        
        for coin in coins:
            for x in range(coin, amount + 1):
                dp[x] = min(dp[x], dp[x - coin] + 1)
        return dp[amount] if dp[amount] != float('inf') else -1 
listi = input().split("")
amount = int(input())
sol = Solution()
print(sol.coinChange(listi,amount))
'''
QUESTION_LANGUAGE = 71

API_URL = 'https://api1.knockouts.dscvit.com/api1/run'
# GET ALL TESTCASES
TESTCASE_GET_URL = "https://api1.knockouts.dscvit.com/api/admin/testcase/get/" + QUESTION_ID + "/"
headers = {
    'authorization': 'Token 641c8d3b9fb9e9f615433e200948dec222d3df75',
    'content-type': 'application/json'
}
testcase_response = requests.request("GET", TESTCASE_GET_URL, headers=headers)
if testcase_response.status_code != 200:
    print("error")
    print(testcase_response.status_code)
    exit()
testcase_response = testcase_response.json()

print("here")
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


def dobase64decode(tobedecoded):
    if tobedecoded is None:
        return "NULL"
    else:
        return base64.b64decode(tobedecoded.encode("ascii"))


total_count = len(testcase_response)
current_count = 0
CODE = base64.b64encode(CODE.encode("ASCII")).decode("ASCII")
for i in testcase_response:
    payload = generatedicti(QUESTION_LANGUAGE, CODE, i['stdin'], i['stdout'])
    response = requests.request("POST", API_URL, headers=headers, json=payload)
    # print(response.text)
    response = response.json()
    # print(response)
    print("Expected STDIN,STDOUT :", i['stdout'], dobase64decode(response['stdout']))
    if response["status"]["id"] == 3:
        current_count += 1
        print("Success :", response["status"]["description"])
    else:
        print("Error :", response["status"]["description"])

if total_count == current_count:
    print("All passed!")
else:
    print("Please reupload question with proper testcases!")
