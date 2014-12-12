from django.contrib.auth.models import User
from django.db import models
from django.utils.html import conditional_escape
import markdown


class DateTimeBase(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PostBase(DateTimeBase):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, null=True, related_name='%(class)s', on_delete=models.SET_NULL)
    content_md = models.TextField(blank=True, null=True)
    bygod = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.bygod = self.bygod if self.author.is_superuser else False
        self.content_md = markdown.markdown(self.content, safe_mode='escape')
        super(PostBase, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class NodeTag(DateTimeBase):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name


class Post(PostBase):
    node = models.ForeignKey(NodeTag, null=True, related_name='posts', on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.title


class Reply(PostBase):
    post_node = models.ForeignKey(Post, null=True, related_name='replies', on_delete=models.SET_NULL)

    def __unicode__(self):
        return "#{0} reply of '{1}'".format(self.pk, self.post_node.title)

    class Meta:
        verbose_name_plural = 'replies'