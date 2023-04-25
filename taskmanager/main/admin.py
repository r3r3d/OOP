from django.contrib import admin
from .models import Task
from .models import AdvUser
from .models import SuperRubric, SubRubric
from .forms import SubRubricForm, OrderForm
from .models import Bb, AdditionalImage

admin.site.register(Task)
admin.site.register(AdvUser)

class SubRubricInline(admin.TabularInline):
   model = SubRubric


class SuperRubricAdmin(admin.ModelAdmin):
   exclude = ('super_rubric',)
   inlines = (SubRubricInline,)

admin.site.register(SuperRubric, SuperRubricAdmin)
class SubRubricAdmin(admin.ModelAdmin):
   form = SubRubricForm


admin.site.register(SubRubric, SubRubricAdmin)


class AdditionalImageInline(admin.TabularInline):
   model = AdditionalImage





class BbAdmin(admin.ModelAdmin):
   form = OrderForm
   list_display = ('rubric', 'title', 'content', 'author', 'created_at', 'imageses', 'commented',)
   fields = (('rubric', 'author'), 'title', 'content',  'status', 'image', 'imageses', 'commented',)
   inlines = (AdditionalImageInline,)

admin.site.register(Bb, BbAdmin)

