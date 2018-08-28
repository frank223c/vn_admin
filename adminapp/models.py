# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
# from django.contrib.gis.geos import Point
STATUSES = (
    (0, 'Disabled'),
    (1, 'Active'),
)

class VNModelBase(models.Model):
    class Meta:
        abstract = True
    original_status = None

    def post_init(self):
        self.original_status = self.status

    def save(self, *args, **kwargs):
        if hasattr(self, 'status') and hasattr(self, 'status_date') and \
            self.status != self.original_status:
            self.status_date = timezone.now()
        return super(VNModelBase, self).save(*args, **kwargs)

    def post_save(self):
        self.original_status = self.status
    
class Customers(VNModelBase):
    name = models.CharField(unique=True, max_length=100)
    address = models.CharField(max_length=256, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True, choices=STATUSES)
    status_date = models.DateTimeField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)
    organization = models.ForeignKey('Organization', models.DO_NOTHING, blank=True, null=True)
    
    class Meta:
        managed = True
        verbose_name_plural = "Customers"
        db_table = 'customers'
        verbose_name = "Customer"
        
    def __str__(self):
        return self.name or ''

class Sites(VNModelBase):
    id = models.PositiveIntegerField(primary_key=True)
    customer = models.ForeignKey(Customers, models.DO_NOTHING)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=256, blank=True, null=True)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    zip_code = models.CharField(max_length=45, blank=True, null=True, choices=STATUSES)
    status = models.IntegerField(blank=True, null=True)
    status_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    operational_time = models.TextField(blank=True, null=True)  # This field type is a guess.
    timezone = models.IntegerField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = True
        verbose_name_plural = "Sites"
        db_table = 'sites'
        verbose_name = "Site"
    
    def full_address(self):
        return "{0}, {1}".format(self.address, self.city)

    def __str__(self):
        return "{0} [{1}]".format(self.name, str(self.customer) if self.customer else 'None')
    
class CraneTypes(VNModelBase):
    id = models.PositiveSmallIntegerField(primary_key=True)
    category = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    vendor = models.CharField(max_length=45, blank=True, null=True)
    model = models.CharField(max_length=45, blank=True, null=True)
    max_load = models.PositiveIntegerField(blank=True, null=True)
 
    class Meta:
        managed = True
        verbose_name_plural = "Crane Types"
        db_table = 'crane_types'
        verbose_name = "Crane Type"
        
    def __str__(self):
        try:
            return str(self.name)
        except:
            return "N/A"
    
class CraneDevices(VNModelBase):
    crane = models.ForeignKey('SiteCranes', models.DO_NOTHING)
    device = models.ForeignKey('Devices', models.DO_NOTHING)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    is_active = models.SmallIntegerField(blank=False, choices=STATUSES)
    class Meta:
        managed = True
        verbose_name_plural = "Crane Devices"
        db_table = 'crane_devices'
        
    @property
    def live_device(self):
        return CraneDevices(end_time=None)
    # live_device.allow_tags = True
    # live_device.short_description = "Live Device"
	    
    def __str__(self):
        return '{0} ,device {1}'.format(str(self.crane) if self.crane else 'None', str(self.device) if self.device else 'None')

class Devices(VNModelBase):
    type = models.IntegerField()
    cranes = models.ManyToManyField(
        'SiteCranes',
        through='CraneDevices',
    )
    create_date = models.DateTimeField(blank=True, null=True,auto_now_add=True)
    status = models.IntegerField(blank=True, null=True,validators=[MinValueValidator(0),MaxValueValidator(1)], choices=STATUSES)
    status_date = models.DateTimeField(blank=True, null=True)
    device_uuid = models.CharField(max_length=20, blank=True, null=True)
    alias = models.CharField(max_length=10, blank=True, null=True)
    device_sw_version = models.FloatField(blank=True, null=True)
    devices_hw_version = models.FloatField(blank=True, null=True)
    device_box_version = models.FloatField(blank=True, null=True)
    device_details = models.TextField(blank=True, null=True)  # This field type is a guess.
    device_parts_sn = models.TextField(blank=True, null=True)  # This field type is a guess
    
    class Meta:
        managed = False
        db_table = 'devices'
        verbose_name_plural = "Devices"
        verbose_name = "Device"
        
    def __str__(self):
        return str(self.alias)+" ("+str(self.device_uuid)+")"
    
    # Check if the status changed, if it does change the status date
    def __init__(self, *args, **kwargs):
        super(Devices, self).__init__(*args, **kwargs)
        self.status_str = "Active" if self.status==1 else "Unactive"

class SiteCranes(VNModelBase):
    site = models.ForeignKey('Sites', models.DO_NOTHING)
    crane_num = models.SmallIntegerField(blank=True, null=True)
    crane_devices = models.ManyToManyField(
        'Devices',
        through='CraneDevices'
    )
    # location = Point(blank=True, null=True)  # This field type is a guess.
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    crane_type = models.ForeignKey(CraneTypes, models.DO_NOTHING, db_column='crane_type', blank=True, null=True)
    max_load = models.PositiveIntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True, choices=STATUSES)
    status_date = models.DateTimeField(blank=True, null=True)

    @property
    def name(self):
         return '{0}, crane {1}'.format(str(self.site), self.crane_num if self.crane_num else 'None')

    class Meta:
        managed = True
        verbose_name_plural = "Cranes"
        db_table = 'site_cranes'    
        verbose_name = "Crane"
        
    def __str__(self):
        return self.name

class AlertNotification(models.Model):
    id = models.BigAutoField(primary_key=True)
    alert = models.ForeignKey('Alerts', models.DO_NOTHING)
    user = models.ForeignKey('People', models.DO_NOTHING)
    notification_channel = models.ForeignKey('NotificationChannel', models.DO_NOTHING, db_column='notification_channel')
    created_at = models.DateTimeField(blank=True, null=True)
    deliverd_at = models.DateTimeField(blank=True, null=True)
    viewed_at = models.DateTimeField(blank=True, null=True)
    user_feedback = models.IntegerField(blank=True, null=True)
    user_comments = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True, choices=STATUSES)
    status_date = models.DateTimeField(blank=True, null=True)
    alert_rule_subscription = models.ForeignKey('AlertRulesSubscription', models.DO_NOTHING, db_column='alert_rule_subscription', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alert_notification'


class AlertRulesSubscription(models.Model):
    alert_rule = models.ForeignKey('SiteKpiAlertRules', models.DO_NOTHING)
    user = models.ForeignKey('People', models.DO_NOTHING)
    notification_channel = models.ForeignKey('NotificationChannel', models.DO_NOTHING, db_column='notification_channel')
    preferences = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'alert_rules_subscription'


class Alerts(models.Model):
    id = models.BigAutoField(primary_key=True)
    message = models.CharField(max_length=256)
    type = models.PositiveIntegerField()
    generation_src = models.CharField(max_length=45)
    generated_by = models.BigIntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True, choices=STATUSES)
    status_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    alert_rule = models.ForeignKey('SiteKpiAlertRules', models.DO_NOTHING, db_column='alert_rule', blank=True, null=True)
    kpi_value = models.ForeignKey('ModuleExecutionPiResults', models.DO_NOTHING, blank=True, null=True)
    site = models.ForeignKey('Sites', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alerts'


class CraneIdleTime(models.Model):
    id = models.BigAutoField(primary_key=True)
    crane = models.ForeignKey('SiteCranes', models.DO_NOTHING)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    pick_cycle = models.ForeignKey('CranePickCycles', models.DO_NOTHING, blank=True, null=True)
    pick_step = models.ForeignKey('CranePickSteps', models.DO_NOTHING, blank=True, null=True)
    is_valid = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crane_idle_time'


class CranePickCyclePhotos(models.Model):
    id = models.BigAutoField(primary_key=True)
    path = models.CharField(max_length=256)
    pick = models.ForeignKey('CranePickCycles', models.DO_NOTHING)
    created_at = models.DateTimeField()
    step = models.ForeignKey('CranePickSteps', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crane_pick_cycle_photos'
        unique_together = (('path', 'pick', 'step'),)


class CranePickCycles(models.Model):
    id = models.BigAutoField(primary_key=True)
    crane = models.ForeignKey('SiteCranes', models.DO_NOTHING)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    load_type = models.ForeignKey('LoadTypes', models.DO_NOTHING, db_column='load_type', blank=True, null=True)
    load_category = models.ForeignKey('LoadCategory', models.DO_NOTHING, db_column='load_category', blank=True, null=True)
    load_weight = models.IntegerField(blank=True, null=True)
    load_from = models.TextField(blank=True, null=True)  # This field type is a guess.
    load_to = models.TextField(blank=True, null=True)  # This field type is a guess.
    accumulative_idle_time = models.IntegerField(blank=True, null=True)
    route = models.TextField(blank=True, null=True)  # This field type is a guess.
    load_alt_from = models.FloatField(blank=True, null=True)
    load_alt_to = models.FloatField(blank=True, null=True)
    product = models.ForeignKey('SiteProducts', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crane_pick_cycles'


class CranePickSteps(models.Model):
    id = models.BigAutoField(primary_key=True)
    pick = models.ForeignKey(CranePickCycles, models.DO_NOTHING)
    step_num = models.PositiveSmallIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    accumulative_idle_time = models.IntegerField(blank=True, null=True)
    from_field = models.TextField(db_column='from', blank=True, null=True)  # Field renamed because it was a Python reserved word. This field type is a guess.
    to = models.TextField(blank=True, null=True)  # This field type is a guess.
    alt_from = models.FloatField(blank=True, null=True)
    alt_to = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crane_pick_steps'
        unique_together = (('pick', 'step_num'),)


class CranePicksTags(models.Model):
    id = models.BigAutoField(primary_key=True)
    pick = models.ForeignKey(CranePickCycles, models.DO_NOTHING, blank=True, null=True)
    step = models.ForeignKey(CranePickSteps, models.DO_NOTHING, blank=True, null=True)
    tagged_by = models.CharField(max_length=20, blank=True, null=True)
    tagged_at = models.DateTimeField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    load_type = models.ForeignKey('LoadTypes', models.DO_NOTHING, db_column='load_type', blank=True, null=True)
    load_category = models.ForeignKey('LoadCategory', models.DO_NOTHING, db_column='load_category', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crane_picks_tags'





class DeviceBatteryHistory(models.Model):
    device = models.ForeignKey('Devices', models.DO_NOTHING, blank=True, null=True)
    battery1_voltage = models.FloatField(blank=True, null=True)
    battery2_voltage = models.FloatField(blank=True, null=True)
    selected_battery = models.IntegerField(blank=True, null=True)
    state_timestamp = models.DateTimeField()
    battery1_bus_voltage = models.FloatField(blank=True, null=True)
    battery2_bus_voltage = models.FloatField(blank=True, null=True)
    battery1_bus_current = models.FloatField(blank=True, null=True)
    battery2_bus_current = models.FloatField(blank=True, null=True)
    battery1_power = models.FloatField(blank=True, null=True)
    battery2_power = models.FloatField(blank=True, null=True)
    battery1_shunt_voltage = models.FloatField(blank=True, null=True)
    battery2_shunt_voltage = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device_battery_history'


class DeviceWeightCalibration(models.Model):
    device = models.ForeignKey('Devices', models.DO_NOTHING)
    offset = models.IntegerField()
    factor = models.FloatField()

    class Meta:
        managed = False
        db_table = 'device_weight_calibration'


class HawkeyeRawdata(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_sn = models.CharField(max_length=16)
    event_timestamp = models.DateTimeField()
    gps_timestamp = models.DateTimeField(blank=True, null=True)
    event_arrival_timestamp = models.DateTimeField(blank=True, null=True)
    gps_lat = models.CharField(max_length=16, blank=True, null=True)
    gps_ns_ind = models.CharField(max_length=1, blank=True, null=True)
    gps_lon = models.CharField(max_length=16, blank=True, null=True)
    gps_ew_ind = models.CharField(max_length=1, blank=True, null=True)
    gps_alt = models.CharField(max_length=16, blank=True, null=True)
    bmp_alt = models.FloatField(blank=True, null=True)
    bmp_tmp = models.FloatField(blank=True, null=True)
    acc_ax = models.FloatField(blank=True, null=True)
    acc_ay = models.FloatField(blank=True, null=True)
    acc_az = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    image_url = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hawkeye_rawdata'


class LoadCategory(models.Model):
    name = models.CharField(unique=True, max_length=100)
    is_material = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'load_category'


class LoadTypes(models.Model):
    name = models.CharField(unique=True, max_length=100)
    category = models.ForeignKey(LoadCategory, models.DO_NOTHING, blank=True, null=True)
    is_material = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'load_types'


class LocationTypes(models.Model):
    name = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'location_types'


class ModuleExecutionPiResults(models.Model):
    id = models.BigAutoField(primary_key=True)
    module_execution = models.ForeignKey('ModulesExecutions', models.DO_NOTHING)
    pi = models.ForeignKey('PiTypes', models.DO_NOTHING)
    pi_value = models.FloatField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    site = models.ForeignKey('Sites', models.DO_NOTHING)
    equipment_id = models.PositiveIntegerField(blank=True, null=True)
    material_id = models.PositiveIntegerField(blank=True, null=True)
    product_id = models.PositiveIntegerField(blank=True, null=True)
    process_id = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    extra_info = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'module_execution_pi_results'


class ModulePermutations(models.Model):
    module = models.ForeignKey('Modules', models.DO_NOTHING)
    version = models.FloatField(blank=True, null=True)
    config = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'module_permutations'


class ModuleRoles(models.Model):
    role = models.ForeignKey('Roles', models.DO_NOTHING)
    module = models.ForeignKey('Modules', models.DO_NOTHING)
    raci = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'module_roles'


class Modules(models.Model):
    type = models.CharField(max_length=45)
    name = models.CharField(max_length=100)
    acronym = models.CharField(max_length=45, blank=True, null=True)
    default_config = models.TextField(blank=True, null=True)  # This field type is a guess.
    latest_version = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'modules'


class ModulesExecutions(models.Model):
    id = models.BigAutoField(primary_key=True)
    module_permutation = models.ForeignKey(ModulePermutations, models.DO_NOTHING)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    execution_entities = models.TextField(blank=True, null=True)  # This field type is a guess.
    result = models.TextField(blank=True, null=True)  # This field type is a guess.
    site = models.ForeignKey('Sites', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'modules_executions'


class ModulesHierarchy(models.Model):
    module = models.ForeignKey(Modules, models.DO_NOTHING, related_name='modules')
    module_child = models.ForeignKey(Modules, models.DO_NOTHING, related_name='modules_child')
    sequnce_num = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'modules_hierarchy'


class NotificationChannel(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'notification_channel'


class OperationalBenchmarks(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    customer = models.ForeignKey(Customers, models.DO_NOTHING, blank=True, null=True)
    site = models.ForeignKey('Sites', models.DO_NOTHING, blank=True, null=True)
    kpi_type = models.ForeignKey('PiTypes', models.DO_NOTHING, db_column='kpi_type')
    upper_bound = models.FloatField(blank=True, null=True)
    lower_bound = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'operational_benchmarks'


class Organization(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)
    type = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'organization'


class People(models.Model):
    site = models.ForeignKey('Sites', models.DO_NOTHING)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    status_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people'


class Permissions(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'permissions'


class PersonOrganizations(models.Model):
    person = models.ForeignKey(People, models.DO_NOTHING)
    organization = models.ForeignKey(Organization, models.DO_NOTHING)
    relation_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'person_organizations'


class PersonRoles(models.Model):
    role = models.ForeignKey('Roles', models.DO_NOTHING)
    person = models.ForeignKey(People, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'person_roles'


class PersonSites(models.Model):
    person = models.ForeignKey(People, models.DO_NOTHING)
    site = models.ForeignKey('Sites', models.DO_NOTHING)
    relation_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'person_sites'


class PiTypes(models.Model):
    name = models.CharField(unique=True, max_length=45)
    description = models.CharField(max_length=255, blank=True, null=True)
    pi_category = models.IntegerField(blank=True, null=True)
    measuring_units = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pi_types'


class ProductDependencies(models.Model):
    id = models.BigAutoField(primary_key=True)
    site = models.ForeignKey('Sites', models.DO_NOTHING)
    product = models.ForeignKey('SiteProducts', models.DO_NOTHING, related_name='product')
    depends_on_product = models.ForeignKey('SiteProducts', models.DO_NOTHING, related_name='depends_on_product')

    class Meta:
        managed = False
        db_table = 'product_dependencies'


class ProductTypes(models.Model):
    name = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'product_types'


class Reports(models.Model):
    id = models.BigIntegerField(primary_key=True)
    site = models.ForeignKey('Sites', models.DO_NOTHING, blank=True, null=True)
    trigger = models.ForeignKey('SiteReportTriggers', models.DO_NOTHING, blank=True, null=True)
    report = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reports'


class RolePermissions(models.Model):
    role = models.ForeignKey('Roles', models.DO_NOTHING)
    permission = models.ForeignKey(Permissions, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'role_permissions'


class Roles(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'roles'


class SiteApis(models.Model):
    site_id = models.PositiveIntegerField(blank=True, null=True)
    type = models.CharField(max_length=45, blank=True, null=True)
    details = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'site_apis'

class SiteKpiAlertRules(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    site = models.ForeignKey('Sites', models.DO_NOTHING)
    kpi_type = models.ForeignKey(PiTypes, models.DO_NOTHING, db_column='kpi_type')
    upper_bound = models.FloatField(blank=True, null=True)
    lower_bound = models.FloatField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    status_date = models.DateTimeField(blank=True, null=True)
    message_template = models.TextField(blank=True, null=True)
    check_interval = models.IntegerField()
    timeframe = models.IntegerField()
    raci = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'site_kpi_alert_rules'


class SiteLocations(models.Model):
    id = models.BigIntegerField(primary_key=True)
    site = models.ForeignKey('Sites', models.DO_NOTHING)
    type = models.ForeignKey(LocationTypes, models.DO_NOTHING, db_column='type', blank=True, null=True)
    location = models.TextField(blank=True, null=True)  # This field type is a guess.
    name = models.CharField(max_length=45, blank=True, null=True)
    buttom_alt = models.FloatField(blank=True, null=True)
    top_alt = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'site_locations'


class SiteMaterialTracking(models.Model):
    id = models.BigAutoField(primary_key=True)
    site = models.ForeignKey('Sites', models.DO_NOTHING, blank=True, null=True)
    load_type = models.ForeignKey(LoadTypes, models.DO_NOTHING, db_column='load_type', blank=True, null=True)
    load_category = models.ForeignKey(LoadCategory, models.DO_NOTHING, db_column='load_category', blank=True, null=True)
    product = models.ForeignKey('SiteProducts', models.DO_NOTHING, blank=True, null=True)
    current = models.IntegerField(blank=True, null=True)
    expected = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'site_material_tracking'


class SiteProducts(models.Model):
    id = models.BigAutoField(primary_key=True)
    site = models.ForeignKey('Sites', models.DO_NOTHING)
    name = models.CharField(max_length=45)
    type = models.ForeignKey(ProductTypes, models.DO_NOTHING, db_column='type')
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)  # This field type is a guess.
    planned_start_time = models.DateTimeField(blank=True, null=True)
    planned_end_time = models.DateTimeField(blank=True, null=True)
    buttom_alt = models.FloatField(blank=True, null=True)
    top_alt = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'site_products'


class SiteReportTriggers(models.Model):
    site_id = models.PositiveIntegerField()
    scheduling = models.TextField()  # This field type is a guess.
    kpis = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'site_report_triggers'


class SiteVendors(models.Model):
    site = models.ForeignKey('Sites', models.DO_NOTHING)
    vendor = models.ForeignKey(Organization, models.DO_NOTHING)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    materials = models.TextField(blank=True, null=True)  # This field type is a guess.
    products = models.TextField(blank=True, null=True)  # This field type is a guess.
    type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'site_vendors'

class UserPermissions(models.Model):
    user = models.ForeignKey(People, models.DO_NOTHING)
    permission = models.ForeignKey(Permissions, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_permissions'