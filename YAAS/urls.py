from django.views.decorators.csrf import csrf_exempt

__author__ = 'Duong Duc Anh'

from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout, password_change_done, password_change
from YAASApp.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'YAAS.views.home', name='home'),
    # url(r'^YAAS/', include('YAAS.foo.urls')),

    url(r'^$', home),
    url(r'^login/$', login_user),
    url(r'^logout/$', logout),
    url(r'^profile/$', user_profile),
    url(r'^register/$', register),
    url(r'^editpassword/$', password_change, {
        'post_change_redirect' : '/editpassword/done/'
    }),
    url(r'^addauction/$', add_auction),
    url(r'^add_auctionConf/$', add_auctionConf),
    url(r'^allauction/$', all_auction),
    url(r'^allauction/(?P<id>\d+)$', post),
    #url(r'^allauction/(?P<id>\d+)$', ),
    url(r'^editpassword/done/$', password_change_done),
    url(r'^editemail/$', change_email),
    url(r'^editdescription/(?P<id>\d+)$', edit_description),
    url(r'^addbid/(?P<id>\d+)$', add_bid),
    #url(r'^translate/$', switch_to_Swedish_link),
    #url(r'^transCheck/$',my_view),
    url(r'^api/search/(?P<title>.+)$', apisearch),
    url(r'^search/$', search),
    url(r'^api/addbid/(\w+)/(\d{1,3})$', csrf_exempt(APIBid())),

    url(r'^vi/$', home_vi),
    #url(r'^register/vi$', register_vi),
    #url(r'^allauction/vi$', all_auction_vi),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
