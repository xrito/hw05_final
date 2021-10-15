from django.contrib import admin

from .models import Comment, Group, Post, Follow


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
        'post_views',
    )
    search_fields = ('text',)
    list_editable = ('group',)
    list_filter = ('pub_date', 'post_views',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class CommentAdmin(admin.ModelAdmin):
    ist_display = (
        'pk',
        'text',
        'create',
        'author',
    )
    search_fields = ('text',)


class FollowAdmin(admin.ModelAdmin):
    ist_display = (
        'User',
        'author',
    )


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
