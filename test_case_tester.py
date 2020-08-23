import json

import requests
import base64

QUESTION_ID = "2be88986-8456-44cb-b13d-21269d0029be"
CODE = '''
#include <iostream>
#include <algorithm>
using namespace std;
int main()
{
                        int intArray[100005];
         long long testcases=1; while(testcases--)
	    	{
                        int N,k;cin>>N>>k;
                        int res =0;
                        for(int i=0;i<N;i++){
                            cin>>intArray[i];
                        }
                        if(N==k){
                            for(int j=0;j<N;j++)
                                res+=intArray[j];
                        }
						else{
                            sort(intArray, intArray+N);
                            res=500000000;
                            int add2=0;
                            for(int i=0;i<k;i++){
                                int add3=0;                                   
                                    for(int n=0;n<k-i;n++){
                                        add3+=intArray[N-n-1];
                                    }
                                int cnt =N-k+1;                                
                                for(int j=N;0<=j-k;j--){
                                    cnt--;                                    
                                    int mult=(i==0)?0:intArray[i-1];
                                  int ans=add2+add3+intArray[j-1]*(N-j)+mult*cnt;
                                  if(ans<res)res=ans;
                                  if(0<=j-(k-i)-1)
                                  add3=add3+intArray[j-(k-i)-1]-intArray[j-1];
                                }
                                add2+=intArray[i];
                            }

                        }cout<<res<<endl;
		}
return 0;
}
'''
QUESTION_LANGUAGE = 54

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
CODE = base64.b64encode((CODE).encode("ASCII")).decode("ASCII")
for i in testcase_response:
    print("Expected STDIN,STDOUT :", i['stdin'], i['stdout'])
    payload = generatedicti(QUESTION_LANGUAGE, CODE, i['stdin'], i['stdout'])
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