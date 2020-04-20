from django.contrib import admin
from .models import Blog
from django.db import models
from blog_index.models import Blog, BlogCategory, BlogSeries


# Register your models here.

class BlogAdmin(admin.ModelAdmin):
	fieldsets = [
		("Title/Author", {"fields":["blog_title","blog_author"]}),
		("URL", {"fields":["blog_slug"]}),
		("Series", {"fields":["blog_series"]}),
		("Content/Date",{"fields":["blog_content","blog_published"]})
	]

admin.site.register(BlogCategory)
admin.site.register(BlogSeries)
admin.site.register(Blog, BlogAdmin)