from django.conf.urls import patterns, include, url
from pexproject.views import *
from django.views.generic.base import RedirectView
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf.urls import handler404
#from pexproject.views import error
#from django.contrib import admin
#admin.autodiscover()
import views



urlpatterns = patterns('',
    #url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', index, name='index'),
    #url(r'^$', 'pexproject.views.index'),
    url(r'', include('social_auth.urls')),
    #url(r'^facebooklogin', facebooklogin, name='facebooklogin'),
    
    url(r'^login', login, name='login'),
    #url(r'^google4fcc5c6791037930', include('webmaster_verification.urls')),
    url(r'^google4fcc5c6791037930$', lambda r: HttpResponse("google-site-verification: google4fcc5c6791037930.html")),
    #url(r'^webmaster', webmaster, name='webmaster'),
    #url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^Admin/$', Admin, name='Admin'),
    url(r'^Admin/adminlogin', adminlogin, name='adminlogin'),
    url(r'^Admin/cityimages', cityimages, name='cityimages'),
    url(r'^Admin/get_cityname', get_cityname, name='get_cityname'),
    url(r'^Admin/manageCityImage', manageCityImage, name='manageCityImage'),
    url(r'^Admin/adminlogout', adminlogout, name='adminlogout'),
    url(r'^Admin/dashboard', dashboard, name='dashboard'),
    url(r'^Admin/bloglist', bloglist, name='bloglist'),
    url(r'^Admin/manageblogImage', manageblogImage, name='manageblogImage'),
    url(r'^Admin/manageBlog', manageBlog, name='manageBlog'),
    url(r'^Admin/manageEmailTemplate', manageEmailTemplate, name='manageEmailTemplate'),
    url(r'^Admin/adimage', adimage, name='adimage'),
    url(r'^Admin/manage_adimage', manage_adimage, name='manage_adimage'),
    url(r'^Admin/pages', pages, name='pages'),
    url(r'^Admin/manage_page', manage_page, name='manage_page'),
    url(r'^Admin/emailTemplate',emailTemplate, name='emailTemplate'),
    url(r'^subscribe', subscribe, name='subscribe'),
    url(r'^blog', blog, name='blog'),
    url(r'^blog/$', blog, name='blog'),
    url(r'^sendFeedBack', sendFeedBack, name='sendFeedBack'),
    url(r'^mailchimp', mailchimp, name='mailchimp'),
    url(r'^createPassword', createPassword, name='createPassword'),
    url(r'^checkData', checkData, name='checkData'),
    url(r'^myRewardPoint', myRewardPoint, name='myRewardPoint'),
    url(r'^manageAccount', manageAccount, name='manageAccount'),
    url(r'^forgotPassword', forgotPassword, name='forgotPassword'),
    url(r'^signup', signup, name='signup'),
    url(r'^staticPage', staticPage, name='staticPage'),
    url(r'^contactUs', contactUs, name='contactUs'),
    url(r'^logout', logout, name='logout'),
    url(r'^flights', flights, name='flights'),
    url(r'^hotels', hotels, name='hotels'),
    url(r'^search_hotel/$', search_hotel),
    url(r'^index', index, name='index'),
    url(r'^searchLoading',searchLoading,name='searchLoading'),
    url(r'^search',search, name='search'),
    url(r'^get_airport', get_airport, name='get_airport'),
    url(r'^getsearchresult', getsearchresult, name='getsearchresult'),
    url(r'^multicity', multicity, name='multicity'),
    url(r'^share', share, name='share'),
    url(r'^filter', filter, name='filter'),
    #url(r'^$','social_auth.urls',namespace='social'),
    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes':True}),
)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
#handler404 = error
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
