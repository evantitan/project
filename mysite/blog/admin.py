from django.contrib import admin
from .models import Post,Comment,Subject,Bookmark
from django_summernote.admin import SummernoteModelAdmin



class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'publish', 'created', 'status', 'subject')
    list_filter = ('publish', 'status')
    prepopulated_fields = {'slug':('title',)}
    summernote_fields = ('body',)


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','user')
    list_filter = ('name','email','user')

admin.site.register(Comment, CommentAdmin)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('topic', 'status')
    list_filter = ('topic', 'status')

admin.site.register(Subject, SubjectAdmin)



class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'post')

admin.site.register(Bookmark, BookmarkAdmin)
