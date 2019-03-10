from django.conf.urls import url ,include
from django.contrib import admin

from annotator.views import resume_list
from annotator.views import annotator_controller
from annotator.views import verify_profile
from annotator.views import clean_username
from annotator.views import user_status
from annotator.resources import UserResource
user_resource = UserResource()
from annotator.resources import ProfileResource
profile_resource = ProfileResource()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^profile/', include(profile_resource.urls)),
    url(r'^user/', include(user_resource.urls)),
    url(r'^user/status', user_status ,name = "status"),
    url(r'^resume/data', resume_list, name='data'),
    url(r'^store/annotations', annotator_controller, name='annotations'),
    url(r'^profile/verify', verify_profile, name='verify'),
    # url(r'^profile/verify/(\w+)/', verify_profile, name='verify'),
    url(r'^cleanusername', clean_username, name='cleanusername'),

]
