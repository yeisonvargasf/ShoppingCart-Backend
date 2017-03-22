from django.conf.urls import url, include
from main.api.v1.urls import my_routers


root_name = 'main'

urlpatterns = [
    url(r'v1/' + root_name + '/', include(my_routers.urls, namespace='v1')),
    url(r'v2/' + root_name + '/', include(my_routers.urls, namespace='v2'))
]
