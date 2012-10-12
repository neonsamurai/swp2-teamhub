from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    # TeamHub custom URLs
    url(r'^$', 'teamhub.views.dashboard', name='home'),
    url(r'^aufgabe/(?P<aufgabeId>\d+)/$', 'teamhub.views.aufgabeDetails' , name='aufgabeDetails'),
    url(r'^profil/','teamhub.views.userProfilBearbeiten'),
    url(r'^projekte/(?P<projektId>\d+)/bearbeiten/$', 'teamhub.views.projektBearbeiten', name='projektBearbeiten'),
    url(r'^projekte/(?P<projektId>\d+)/$', 'teamhub.views.projektDetail', name='projektDetails'),
    url(r'^projekte/','teamhub.views.projektListe'),
    url(r'^login/','django.contrib.auth.views.login'),
    url(r'^logout/','teamhub.views.logoutUser'),
    # Examples:
    # url(r'^project_settings/', include('project_settings.foo.urls')),

    # Admin urls
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    # Comments framework urls
    url(r'^comments/', include('django.contrib.comments.urls')),
)
