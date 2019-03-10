from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from annotator.models import profiles
from annotator.models import intermidiate
from annotator.models import processed
from annotator.models import temp_annotated_data
from annotator.models import approver_annotated_data
from annotator.models import user
from django.core import serializers
import random
from django.db.models import Count
from django.db.models import Q
import json
import time
from urllib.parse import unquote

from django.template import Context, loader ,RequestContext
from django.shortcuts import render_to_response

class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class ErrorResponse(HttpResponse):   
    def my_test_500_view(request):
        return HttpResponse("internal server error",status=500)         

def resume_list(request):
    if request.method == 'GET':
        try:
            print("*************************************** getting random resume *******************************************")
            urlname = request.get_full_path()
            _resumeId = urlname.split('/')[-1]
            print(_resumeId)
            if _resumeId != 'data':
                _username = request.META['HTTP_USERNAME']
                return getResumeBasedOnId(_resumeId ,_username)
            else :    
                _checker = False
                _username = request.META['HTTP_USERNAME']
                _ids = profiles.objects.filter(tempUserId='').values('id')
                # _ids = profiles.objects.values('id')
                _size = len(_ids)
                print("first _size  --> ",_size)
                print("first _size == 0  --> ", _size == 0)
                tableSelector = random.randint(1, 4)
                if _size == 0 or tableSelector == 4:
                    _inter_ids = intermidiate.objects.filter(~Q(userName=_username) ,tempUserId='').values('id')
                    _inter_size = len(_inter_ids)
                    if _inter_size != 0:
                        _checker = True
                        return pickFormIntermidiate(_username ,_inter_size ,_inter_ids)
                    elif _size != 0:
                        _checker = True
                        return pickNewResume(_username,_size,_ids)
                else :
                    _checker = True
                    return pickNewResume(_username,_size,_ids)
        except:       
            return  JSONResponse({"data":"no data found"})
        if _checker == False :
            return  JSONResponse({"resume":"All resumes are annotated"})

def getResumeBasedOnId(_resumeId , _username):
    _check = False
    _approver = False
    test = ""
    _resumeId = unquote(_resumeId)
    print("********************getting old resume*******************" ,_resumeId) 
    count = profiles.objects.filter(resumeId=_resumeId).count()
    print("count--->",count)
    if count > 0:
        test = profiles.objects.filter(resumeId=_resumeId)
        _check = True
    else : 
        count = intermidiate.objects.filter(resumeId=_resumeId).count() 
        if count > 0:
            test = intermidiate.objects.filter(resumeId=_resumeId)
            _check = True
            _approver = True
    if _check == True:
        print("checker true  =====================")
        json_data = serializers.serialize("json", test)
        readable_json = json.loads(json_data)
        response_array = {
            'resumeId' : readable_json[0]['fields']['resumeId'],
            'resume' : readable_json[0]['fields']['resume'],
            'userName' : _username
        }
        if _username == readable_json[0]['fields']['tempUserId']  and _approver == True:
            response_array['approverName'] = readable_json[0]['fields']['tempUserId']
            response_array['userName'] = readable_json[0]['fields']['userName']

        print("Got the resume for =====================" ,_username)
        return JSONResponse(response_array)

    return JSONResponse({"data":"no data found"})

def pickNewResume(username,_size,_ids) :
    print("********************************** picking new resume ****************************")
    pkId = random.randint(1, _size)
    pkId =_ids[pkId-1]['id']
    print("pkId is --> ",pkId)
    test = profiles.objects.filter(id=pkId)
    json_data = serializers.serialize("json", test)
    readable_json = json.loads(json_data)
    profiles.objects.filter(id=pkId).update(tempUserId=username)
    response_array = {
        'resumeId' : readable_json[0]['fields']['resumeId'],
        'resume' : readable_json[0]['fields']['resume'],
        'userName' : username
    }
    
    return JSONResponse(response_array)
    
def pickFormIntermidiate(username ,_size,_ids):
    print("in processded   --------> ",username)
    if _size != 0:
        pkId = random.randint(1, _size)
        pkId =_ids[pkId-1]['id']
        print("pkId is --> ",pkId)
        test = intermidiate.objects.filter(id=pkId)
        print("befire sadsadsad-------------------------------------------------")
        json_data = serializers.serialize("json", test)
        readable_json = json.loads(json_data)
        intermidiate.objects.filter(id=pkId).update(tempUserId=username)
        response_array = {
            'resumeId' : readable_json[0]['fields']['resumeId'],
            'resume' : readable_json[0]['fields']['resume'],
            'userName' : readable_json[0]['fields']['userName'],
            'approverName' : username
        } 
        return JSONResponse(response_array)

def track_user_action(_resumeId,_tagId,body_unicode,_approvername,_action):
    print("track_user_action check ")
    count = intermidiate.objects.filter(resumeId=_resumeId).count()
    print("count--->",count)
    if count > 0:
        print("moving data for backup")
        deleted_data = temp_annotated_data.objects.filter(resumeId=_resumeId , tagId=_tagId)
        json_data = serializers.serialize("json", deleted_data)
        readable_json = json.loads(json_data)
        if body_unicode == "":
            body_unicode = readable_json[0]['fields']['annotaedData']
        _username = readable_json[0]['fields']['userName']  
        data = approver_annotated_data(resumeId = _resumeId , approverName = _approvername ,tagId = _tagId,annotaedData=body_unicode,action =_action,userName=_username)
        data.save()
            

def annotator_controller(request):
    json_data ={"data":"no data found"}
    if request.method == 'PUT':
        print("****************  inside PUT Method Annotator *****************")
        urlname = request.get_full_path()
        body_unicode = request.body.decode('utf-8')
        print("annptator controller put",body_unicode)
        body = json.loads(body_unicode)
        _resumeId = urlname.split('/')[-2]
        _resumeId = unquote(_resumeId)
        _tagId = urlname.split('/')[-1]
        _username = request.META['HTTP_USERNAME']
        track_user_action(_resumeId,_tagId,body_unicode,_username,"update")
        temp_annotated_data.objects.filter(resumeId=_resumeId , tagId=_tagId).update(annotaedData=body_unicode , userName = _username)
        json_data = {"status":"data updated sucessfully","id" : _tagId}
    elif request.method == 'POST':
        print("****************  inside POST Method Annotator *****************")
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        _username = request.META['HTTP_USERNAME']
        _resumeId = body['resumeId']
        body['id'] = int(round(time.time() * 1000))
        body_unicode  = json.dumps(body)
        data = temp_annotated_data(resumeId = _resumeId , userName = _username ,tagId = body['id'],annotaedData=body_unicode)
        data.save()
        processOtherTables(_username , _resumeId)
        json_data = {"status":"data saved sucessfully","id" : body['id']}
    elif request.method == 'DELETE':
        print("****************  inside DELETE Method Annotator *****************")
        urlname = request.get_full_path()
        _resumeId =urlname.split('/')[-2]
        _resumeId = unquote(_resumeId)
        _tagId = urlname.split('/')[-1]
        _username = request.META['HTTP_USERNAME']
        track_user_action(_resumeId,_tagId,"",_username,"delete")
        json_data = temp_annotated_data.objects.filter(resumeId=_resumeId , tagId=_tagId).delete() 
        json_data = {"status":"data deleted sucessfully"}
    elif request.method == 'GET':
        try :
            print("****************  inside GET Method Annotator *****************")
            urlname = request.get_full_path()
            _resumeId = urlname.split('/')[-1]    #request.META['HTTP_RESUMEID']
            _resumeId = unquote(_resumeId)
            json_data = temp_annotated_data.objects.values('annotaedData').filter(resumeId=_resumeId)
            print('json --> ',json_data)
            response_json = {}
            response_array = []
            count = 0
            for data in json_data:
                response_array.append(json.loads(data['annotaedData']))     
            response_json['rows'] = response_array
            json_data = response_json
        except Exception as ex:
            print("got exception ====================================================== ", ex)
            return ErrorResponse("internal server error").my_test_500_view()               

    print("Done with computation of crud ",json_data)
    return  JSONResponse(json_data)
def processOtherTables(_username , _resumeId):
    print("processing data")
    count = profiles.objects.filter(resumeId=_resumeId).count()
    if count > 0 :
        test = profiles.objects.filter(resumeId=_resumeId)
        print("************************first table data moving ***********************************")
        json_data = serializers.serialize("json", test)
        readable_json = json.loads(json_data)
        inter = intermidiate(resumeId = readable_json[0]['fields']['resumeId'] , resume = readable_json[0]['fields']['resume'],userName=_username)
        inter.save()
        profiles.objects.filter(resumeId=_resumeId).delete()
    

def user_status(request):
    json_data ={"data":"no data found"}
    print("********************************** under user status ******************************")
    urlname = request.get_full_path()
    loginkey = urlname.split('/')[-1]
    username = urlname.split('/')[-2]
    if (loginkey != ""):
        json_data = user.objects.filter(loginKey=loginkey , userName=username).update(loginKey="")
    if(json_data == 1):
        print("((((((((((((((((((((((((((((((((((((true")
        json_data ={"auth":True}
    else:
        print("((((((((((((((((((((((((((((((((((((false")
        json_data ={"auth":False}

    return  JSONResponse(json_data)


def verify_profile(request):
    response_data ={"data":"no data found"}
    if request.method == 'PUT':
        urlname = request.get_full_path()
        _resumeId = urlname.split('/')[-1]
        _resumeId = unquote(_resumeId)
        _username = request.META['HTTP_USERNAME']
        print("********************************** verifying resume ******************************",_resumeId)
        count1 = intermidiate.objects.filter(resumeId=_resumeId).count()
        if count1 > 0 :
            test1 = intermidiate.objects.filter(resumeId=_resumeId)
            print("intermediate table data moving")
            json_data = serializers.serialize("json", test1)
            readable_json = json.loads(json_data)
            procesed = processed(resumeId = readable_json[0]['fields']['resumeId'] , resume = readable_json[0]['fields']['resume'],userName=readable_json[0]['fields']['userName'],approverName=_username)
            procesed.save()
            intermidiate.objects.filter(resumeId=_resumeId).delete()
            response_data = {"verified":"true"}

    return  JSONResponse(response_data)


def clean_username(request):
    print("********************************** cleaning username ************************************")
    profiles.objects.filter(~Q(tempUserId='')).update(tempUserId='')
    intermidiate.objects.filter(~Q(tempUserId='')).update(tempUserId='')
    return  JSONResponse({"done":"kya karega ab delte ho gya data"})

# working with retry logic
# def resume_list(request):
#     if request.method == 'GET':
#         _size = len(profiles.objects.values('id'))
#         pkId = random.randint(1, _size)
#         print("pkId is --> ",pkId)
#         print("profiles.objects.filter(id=pkId , ~Q(resumeId='picked'))", profiles.objects.filter(~Q(resumeId='picked'),id=pkId))
#         _checker = 0
#         while not profiles.objects.filter(~Q(resumeId='picked'),id=pkId) and _checker < 5 :
#             print("inside while picked the wrong one")
#             checker = checker + 1
#             pkId = random.randint(1, _size)        
#         test = profiles.objects.filter(~Q(resumeId='picked'),id=pkId)
#         profiles.objects.filter(id=pkId).update(resumeId='picked')
#         return JSONResponse(serializers.serialize("json", test))