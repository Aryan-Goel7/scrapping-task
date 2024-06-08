from scrapper_app.views import ScrapperList
from django.urls import path

urlpatterns = [
    path('scrap/',ScrapperList.as_view()),
]
 