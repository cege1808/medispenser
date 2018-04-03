from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Medication, Schedule, Log

# Register your models here.
class LogUserInline(admin.TabularInline):
    model = Log
    can_delete = True
    verbose_name_plural = 'Logs'
    fk_name = 'user'
    extra = 1

class LogMedInline(admin.TabularInline):
    model = Log
    can_delete = True
    verbose_name_plural = 'Logs'
    fk_name = 'medication'
    extra = 1

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class MedicationInline(admin.TabularInline):
    model = Medication
    can_delete = True
    verbose_name_plural = 'Medications'
    fk_name = 'user'
    extra = 1

class ScheduleInline(admin.TabularInline):
    model = Schedule
    can_delete = True
    verbose_name_plural = 'Schedules'
    fk_name = 'user'
    extra = 1

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, MedicationInline, ScheduleInline, LogUserInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_select_related = ('profile',)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

class MedicationAdmin(admin.ModelAdmin):
    inlines = (LogMedInline, )
    list_display = ('pk', 'pill_name', 'module_num', 'user', )

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'module_nums', 'category', 'day', 'time', 'counter',)

class LogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created_at', 'user', 'medication')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Medication, MedicationAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Log, LogAdmin)
