from django.urls import path, include


app_name = 'api'
urlpatterns = [
    path('profile/', include('userprofile.urls')),
]
