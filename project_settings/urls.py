from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    
    # TeamHub custom URLs
    url(r'^$', 'teamhub.views.dashboard', name='home'),
    url(r'^aufgabe/(?P<aufgabeId>\d+)/$', 'teamhub.views.aufgabeDetails' , name='aufgabeDetails'),
    url(r'^aufgabe/offeneAufgaben/', 'teamhub.views.offeneAufgabenAnzeigen'),
    url(r'^aufgabe/vonMirErstellteAufgaben/', 'teamhub.views.vonMirErstellteAufgaben'),
    url(r'^profil/','teamhub.views.userProfilBearbeiten'),
    url(r'^projekte/(?P<projektId>\d+)/bearbeiten/$', 'teamhub.views.projektBearbeiten', name='projektBearbeiten'),
    url(r'^projekte/(?P<projektId>\d+)/$', 'teamhub.views.projektDetail', name='projektDetails'),
    url(r'^aufgabe/(?P<aufgabeId>\d+)/bearbeiten/$', 'teamhub.views.aufgabeBearbeiten', name='aufgabeBearbeiten'),
    url(r'^aufgabe/(?P<aufgabeId>\d+)/aufgabeAnnehmen/$', 'teamhub.views.aufgabeAnnehmen' , name='aufgabeAnnehemn'),
    url(r'^projekte/erstellen/','teamhub.views.projektErstellen'),
    url(r'^aufgabe/erstellen/','teamhub.views.aufgabeErstellen'),
    url(r'^projekte/','teamhub.views.projektListe'),
    url(r'^aufgabe/','teamhub.views.aufgabe'),
    url(r'^login/','django.contrib.auth.views.login'),
    url(r'^logout/','teamhub.views.logoutUser'),
    url(r'^benutzer/','teamhub.views.benutzerErstellen'),
    url(r'^suchen/','teamhub.views.search'),
    url(r'^passwaendern/','teamhub.views.passwortAendern'),
    # Examples:
    # url(r'^project_settings/', include('project_settings.foo.urls')),

    # Admin urls
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    
    # Comments framework urls
    url(r'^comments/', include('django.contrib.comments.urls')),
    
)
