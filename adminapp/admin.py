from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from django.urls import reverse
from django.conf.urls import url
from .forms import AddForm
import code

# Register your models here.
from .models import *
from django.contrib.auth.admin import UserAdmin

def swap_function(modeladmin, request, queryset):
	print("queryset :",queryset)
	print("length :",len(queryset))
	if len(queryset)!=2:
		modeladmin.message_user(request = request, message = "To swap devices, please select exactly 2 cranes.", level=messages.ERROR)
		return
	else:
		crane1, crane2 = queryset.first(),queryset.last()
		device1, device2 = crane1.device,crane2.device
		crane1.device = device2
		crane2.device = device1
		crane1.save()
		crane2.save()
		modeladmin.message_user(request = request, message = "Devices swapped successfully")

swap_function.short_description = "Swap devices of the selected cranes"

class VNBaseAdmin(admin.ModelAdmin):
	exclude = ('status_date',)

class CraneDevicesAdmin(VNBaseAdmin):
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == "device":
			new_queryset = Devices.objects.exclude(id__in=CraneDevices.objects.values('device_id').query)
			print(new_queryset)
			kwargs["queryset"] = new_queryset
		return super(CraneDevicesAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
			
	#Enabling swap function
	list_display = ['crane', 'device']
	ordering = ['crane']
	actions = [swap_function]


class AddDisabled(VNBaseAdmin):
	def has_add_permission(self, request):
		return False

class DeviceAdmin(VNBaseAdmin):
	fields = ["alias","device_uuid","type","status"]

	def status_str(self,obj):
		return "Alive" if obj.status == 1 else "Dead"
	status_str.short_description = 'Status'
	
	list_display = (
        'alias',
        'device_uuid',
		'status_str'
        #'device_actions', 
    )

	# def process_add(self, request, device_id, *args, **kwargs):
		# return self.process_action(
			# request=request,
			# device_id=device_id,
			# action_form=AddForm,
			# action_title='Add Device',
		# )
		
	# def get_urls(self):
		# urls = super().get_urls()
		# custom_urls = [
			# url(
				# r'^(?P<device_id>.+)/add/$',
				# self.admin_site.admin_view(self.process_add),
				# name='enable_device',
			# ),
		# ]
		# return custom_urls + urls

	# def device_actions(self, obj):
		# return format_html(
			# '<a class="button" href="{}">Add device</a>&nbsp;',
			# reverse('admin:enable_device', args=[obj.pk]),
		# )
		
	# device_actions.short_description = 'Device Status'
	# device_actions.allow_tags = True
	
#class SiteCraneAdmin(admin.ModelAdmin):
	
class CraneAdmin(VNBaseAdmin):
	list_display = (
        'crane_num',
        'site',
		'status_str',
		'device'
    )

	def status_str(self,obj):
		return "Active" if obj.status == 1 else "Inactive"
	status_str.short_description = 'Status'
	
class CraneDevicesFilters(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = "Crane-Device correlation (Default: Active devices)"
    parameter_name='crane_device_filter'

    def lookups(self, request, model_admin):
        return (
            ('InactiveDevice', 'Inactive devices'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        cranes_with_active_devices = queryset.exclude(cranedevices__device=None).filter(cranedevices__is_active=True)
        cranes_with_active_devices_ids = list(map(lambda x: x.id, cranes_with_active_devices))
        if self.value() == 'InactiveDevice':
            return queryset.exclude(id__in=cranes_with_active_devices_ids)
        return queryset.exclude(cranedevices__device=None).filter(cranedevices__is_active=True)

class CraneDevicesInline(admin.TabularInline):
    model = CraneDevices
    extra = 0
    actions = [swap_function]
    def get_queryset(self, request):
        qs = super(CraneDevicesInline, self).get_queryset(request)
        crane_id=int(request.resolver_match.kwargs['object_id'])
        return qs.filter(crane_id=crane_id).exclude(device=None).order_by('-is_active', '-id')
class SiteCranesAdmin(VNBaseAdmin):
    inlines = [CraneDevicesInline]
    exclude = ['devices', 'status_date']
    list_filter = (CraneDevicesFilters,)
    search_fields = ('site__name','site__address','site__city', 'crane_num')


#admin.site.register(UserAdmin)
admin.site.register(Customers)
admin.site.register(Sites)
admin.site.register(SiteCranes, SiteCranesAdmin)

add_a_device = True
admin.site.register(Devices,DeviceAdmin)
# admin.site.register(CraneDevices, CraneDevicesAdmin)
