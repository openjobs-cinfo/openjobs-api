from django.contrib import admin
from .models import User, Degree, Job, Skill, DataOrigin, Address, Qualification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = (
        'email', 'name', 'avatar_url', 'birth_date', 'address_id', 'skills', 'qualifications', 'is_staff', 'is_active',
        'is_superuser', 'groups', 'user_permissions', 'last_login', 'date_joined'
    )
    exclude = ('password',)
    readonly_fields = ('last_login', 'date_joined')


admin.site.register(Degree)
admin.site.register(Job)
admin.site.register(Skill)
admin.site.register(DataOrigin)
admin.site.register(Address)
admin.site.register(Qualification)
