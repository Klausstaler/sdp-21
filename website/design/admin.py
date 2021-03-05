from django.contrib import admin

# Register your models here.

from .models import node,shelf,package,robot,task,hidden_package


class nodeAdmin(admin.ModelAdmin):

    class Meta:
        model = node
admin.site.register(node,nodeAdmin)

class packageAdmin(admin.ModelAdmin):
    list_display = ['id','shelf','shelf_compartment']
    class Meta:
        model = package
admin.site.register(package,packageAdmin)

class robotAdmin(admin.ModelAdmin):
    list_display = ['name','ip']
    class Meta:
        model = robot
admin.site.register(robot,robotAdmin)

class shelfAdmin(admin.ModelAdmin):
    list_display = ['id','node']
    class Meta:
        model = shelf
admin.site.register(shelf,shelfAdmin)
#admin.site.register(task)
#admin.site.register(hidden_package)