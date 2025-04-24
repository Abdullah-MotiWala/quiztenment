from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

# 'about' , 

class StaticViewSitemap(Sitemap):
	def items(self):
		return ['home' , 'about' ,   'policy' , 'faq' ,'terms' , 'contact' ]
		
	def location(self, item):
		return reverse(item)
		


