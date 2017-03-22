from django.conf.urls import url, include

import main.api.urls as api_urls

urlpatterns = [
    url(r'', include(api_urls)),
]
