-----------------------------------------------------------------------------------------------------
										User/Login Related Calls
-----------------------------------------------------------------------------------------------------	
	
GET Call --> to validate the user
http://127.0.0.1:8000/user/status/{username}/{key}
Response -->
{
    "auth": "false"
} or
{
    "auth": "true"
}
-----------------------------------------------------------------------------------------------------
								Get The Resume Text with important annotation 
-----------------------------------------------------------------------------------------------------
GET Call --> To get the whole resume text
http://127.0.0.1:8000/resume/data
Hearderparam -->
Content-Type : application/json
username : {userName}

If no result found
Response -->
{
    "resume": "All resumes are annotated"
}
If resume for first time 
{
    "resumeId": "test3",
    "resume": "full text",
    "userName": "gjangra"
}
If resume for approver time 
{
    "resumeId": "test3",
    "resume": "full text",
    "userName": "gjangra",
	"approverName" : "gjangra"
}

-----------------------------------------------------------------------------------------------------
								EndPoint Related to annotated data
-----------------------------------------------------------------------------------------------------

POST Call --> to add new annotated data 
http://127.0.0.1:8000/store/annotations
Hearderparam -->
Content-Type : application/json
username : {userName}
body -->
{"ranges":[{"start":"/p[1]","startOffset":1270,"end":"/p[1]","endOffset":1294}],"quote":"test","category":"test","text":"test","id":3,"resumeId":"GouravResume2"}
Response -->
{
    "status": "data saved sucessfully"
}


GET Call --> To get all the annotated data for one resume
http://127.0.0.1:8000/store/annotations/{resumeId}

Response -->
{
    "rows": [
        "{'ranges': [{'start': '/p[1]', 'startOffset': 1270, 'end': '/p[1]', 'endOffset': 1294}], 'quote': 'Gourav Jan', 'category': 'Full Name', 'text': '2changed', 'id': 1, 'resumeId': 'GouravResume1'}",
        "{'ranges': [{'start': '/p[1]', 'startOffset': 1270, 'end': '/p[1]', 'endOffset': 1294}], 'quote': 'Cognizant', 'category': 'Company', 'text': 'company', 'id': 1, 'resumeId': 'GouravResume1'}"
    ]
}

PUT Call --> 
http://127.0.0.1:8000/store/annotations/{resumeId}/{tagId}
body -->
{"ranges":[{"start":"/p[1]","startOffset":1270,"end":"/p[1]","endOffset":1294}],"quote":"Gourav Jan3","category":"Full Name","text":"changed3","id":3,"resumeId":"GouravResume3"}

Response -->
{
    "status": "data updated sucessfully"
}

Delete Call -->
http://127.0.0.1:8000/store/annotations/{resumeId}/{tagId}
{
    "status": "data deleted sucessfully"
}