from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    # TeamHub custom URLs
    url(r'^$', 'teamhub.views.dashboard', name='home'),
    url(r'^aufgabe/(?P<aufgabeId>\d+)/$', 'teamhub.views.aufgabeDetails' ,name='aufgabeDetails'),
    url(r'^login/','django.contrib.auth.views.login'),
    url(r'^logout/','teamhub.views.logoutUser'),
    #url(r'^logout/','teamhub.views.logout'),
    # Examples:
    # url(r'^project_settings/', include('project_settings.foo.urls')),

    # Admin urls
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    # Comments framework urls
    url(r'^comments/', include('django.contrib.comments.urls')),
)
