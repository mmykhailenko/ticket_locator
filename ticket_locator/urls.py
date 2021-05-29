from django.contrib import admin
from django.urls import path, include

from hello_world import urls, views
from ticket_locator.urls_swagger import urlpatterns as swagger

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/', include(urls)),
	path('', views.SearchView.as_view(), name='searchViewPage')
]

urlpatterns += swagger
print(urlpatterns)