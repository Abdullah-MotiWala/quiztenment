# from django.conf.urls import url
from django.urls import re_path as url
from django.conf import settings
from django.views.static import serve

from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from core.sitemap import StaticViewSitemap
from django.contrib.sitemaps.views import sitemap




from django.views.generic.base import TemplateView #import TemplateView





sitemaps = {
	'static': StaticViewSitemap,
}

urlpatterns = [

	url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),

	url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

	path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
	name='django.contrib.sitemaps.views.sitemap'),

	path("robots.txt",TemplateView.as_view(template_name="core/robots.txt", content_type="text/plain")),  #add the robots.txt file


	path('admin/', admin.site.urls),
	path('', include("core.urls")),
	path('ckeditor/', include('ckeditor_uploader.urls')), 


]
#### 404 page   ######33
handler404 = 'core.views.error_404_view'
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 


