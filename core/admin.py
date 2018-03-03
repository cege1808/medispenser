from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Medication, Schedule

# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class MedicationInline(admin.StackedInline):
    model = Medication
    can_delete = True
    verbose_name_plural = 'Medications'
    fk_name = 'user'
    extra = 1

class ScheduleInline(admin.StackedInline):
    model = Schedule
    can_delete = True
    verbose_name_plural = 'Schedules'
    fk_name = 'user'
    extra = 1

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, MedicationInline, ScheduleInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_select_related = ('profile',)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Medication)
admin.site.register(Schedule)