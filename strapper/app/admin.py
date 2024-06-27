from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from unfold.decorators import display
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _
from unfold.views import UnfoldModelAdminViewMixin
from django.views.generic import TemplateView

# Register your models here.
admin.site.site_header = "Admin Panel"

from app.models import User, JobPreference,JobOpted,Review,Jobs

class UserStatus(TextChoices):
    ACTIVE = "ACTIVE", _("Active")
    PENDING = "PENDING", _("Pending")
    INACTIVE = "INACTIVE", _("Inactive")
    CANCELLED = "CANCELLED", _("Cancelled")

class MyClassBasedView(UnfoldModelAdminViewMixin, TemplateView):
    title = "Custom Title"  # required: custom page header title
    permissions_required = () # required: tuple of permissions
    template_name = "some/template/path.html"
    
@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display=("user_id","message","rating")
    
@admin.register(Jobs)
class JobAdmin(ModelAdmin):
    list_display=('title','description','location','link','company','job_type') 
    search_fields=('title','location','company')
    
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
        result = obj.jobid.title
        return result
    
