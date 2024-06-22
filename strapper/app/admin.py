from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from unfold.decorators import display
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _
from unfold.views import UnfoldModelAdminViewMixin
from django.views.generic import TemplateView
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm



# Register your models here.
admin.site.site_header = "Admin Panel"

from app.models import Person, Course, Grade, User, JobPreference,JobOpted

class UserStatus(TextChoices):
    ACTIVE = "ACTIVE", _("Active")
    PENDING = "PENDING", _("Pending")
    INACTIVE = "INACTIVE", _("Inactive")
    CANCELLED = "CANCELLED", _("Cancelled")

class MyClassBasedView(UnfoldModelAdminViewMixin, TemplateView):
    title = "Custom Title"  # required: custom page header title
    permissions_required = () # required: tuple of permissions
    template_name = "some/template/path.html"
    
@admin.register(JobPreference)
class JobPreferenceAdmin(ModelAdmin):
    list_display = ("id","title","job_code")
    search_fields=('title',)

@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display=("name","password","email","image","description","hash","location")
    search_fields=("name",)
    list_filter=("name",)
    
@admin.register(JobOpted)
class JobOptedAdmin(ModelAdmin):
    list_display=("id","user","job")
    search_fields=("id",)
    
    def user(self,obj):
        result = User.objects.filter(id=obj.user_id.id).first()
        return result.name
    
    def job(self,obj):
        result = JobPreference.objects.filter(id=obj.id).first()
        return result.title
    
    
        """_summary_
@admin.register(Person)
class PersonAdmin(ModelAdmin):
    list_display=("last_name","first_name","show_average")
    search_fields=("first_name",)
    list_filter=("first_name",)
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    
        
    def show_average(self, obj):
        from django.db.models import Avg
        result = Grade.objects.filter(person=obj).aggregate(Avg("grade"))
        return result["grade__avg"]
    
    show_average.short_description="Average grade"

    @display(
        description=_("Status"),
        ordering="status",
        label={
            UserStatus.ACTIVE: "success",  # green
            UserStatus.PENDING: "info",  # blue
            UserStatus.INACTIVE: "warning",  # orange
            UserStatus.CANCELLED: "danger",  # red
        },
    )
    
    def show_status(self, obj):
        return obj.status

    @display(description=_("Status with label"), ordering="status", label=True)
    def show_status_with_custom_label(self, obj):
        return obj.status, obj.get_status_display()

    @display(header=True)
    def display_as_two_line_heading(self, obj):
        return "First main heading", "Smaller additional description"
"""
