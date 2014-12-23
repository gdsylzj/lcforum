# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Post, Reply, NodeTag

# Register your models here.

admin.site.register(Post)
admin.site.register(Reply)
admin.site.register(NodeTag)
