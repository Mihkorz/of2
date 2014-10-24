from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile, Project, Document

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'
    
# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class ProjectAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'owner', 'description', 'status', 'field', 'created_at' )
    list_filter = ['owner']
    exclude = ('members',)

admin.site.register(Project, ProjectAdmin)

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('get_filename', 'project', 'created_by', 'created_at')

admin.site.register(Document, DocumentAdmin) 
