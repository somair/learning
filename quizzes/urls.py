from django.conf.urls import url
from . import views

#Acces to this routes using /quizzes/urlpattern
urlpatterns = [
    #Quizzes home
    url(r'^$', views.index, name='index'),
    #List decks
    url(r'^list/$', views.listing, name='listing'),
    #Add a new deck
    url(r'^new/$', views.new, name='new'),
    #Do a quiz
    url(r'^detail/(?P<deck_id>.+)/$', views.detail, name='detail'),
    #See results (renders html)
    url(r'^results/(?P<deck_id>.+)/$', views.results, name='results'),
    #Fetch results form db and return json data
    url(r'^fetch_results/(?P<deck_id>.+)/$', views.fetch_results, name='fetch_results'),
    #Save a result
    url(r'^save/$', views.save, name='save'),
]