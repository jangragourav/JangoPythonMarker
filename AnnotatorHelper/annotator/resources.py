from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from annotator.models import profiles
from annotator.models import user
from django.db.models import Max
import random
  

class ProfileResource(ModelResource):
    class Meta:
        queryset = profiles.objects.all()
        resource_name = 'store'
        authorization = Authorization()
    

class UserResource(ModelResource): 
    class Meta:
        queryset = user.objects.all()
        list_allowed_methods = ['post']
        resource_name = 'store'
        always_return_data = True
        fields = ['userName','loginKey']
        filtering = {
            'loginKey': ("exact",),
        }
        authorization = Authorization()