from django.db import models

# Create your models here.

direction_choices = (
    ('bi','bi'),
    ('from','from'),
    ('to','to')
)

class node(models.Model):
    id = models.AutoField(primary_key=True)
    right_node = models.ForeignKey('self',on_delete=models.CASCADE, related_name="right",blank=True, null=True)
    right_node_distance = models.IntegerField(verbose_name='Right node distance',blank=True, null=True)
    right_node_direction = models.CharField(max_length=6,choices=direction_choices,blank=True, null=True)
    right_node_priority = models.IntegerField(blank=True, null=True)
    down_node = models.ForeignKey('self',on_delete=models.CASCADE, related_name="down",blank=True, null=True)
    down_node_distance = models.IntegerField(verbose_name='Down node distance',blank=True, null=True)
    down_node_direction = models.CharField(max_length=6,choices=direction_choices,blank=True, null=True)
    down_node_priority = models.IntegerField(blank=True, null=True)
    left_node = models.ForeignKey('self',on_delete=models.CASCADE, related_name="left",blank=True, null=True)
    left_node_distance = models.IntegerField(verbose_name='Left node distance',blank=True, null=True)
    left_node_direction = models.CharField(max_length=6,choices=direction_choices,blank=True, null=True)
    left_node_priority = models.IntegerField(blank=True, null=True)
    up_node = models.ForeignKey('self',on_delete=models.CASCADE, related_name="up",blank=True, null=True)
    up_node_distance = models.IntegerField(verbose_name='Up node distance',blank=True, null=True)
    up_node_direction = models.CharField(max_length=6,choices=direction_choices,blank=True, null=True)
    up_node_priority = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return str(self.id)
class shelf(models.Model):
    id = models.AutoField(primary_key=True)
    node = models.ForeignKey(node,on_delete=models.CASCADE, related_name="Node")
    number_of_compartments = models.IntegerField(verbose_name='Compartments')
    compartment_size = models.IntegerField(verbose_name='Compartment_size')
    class Meta:
        verbose_name_plural = 'Shelves'
    def __str__(self):
        return str(self.id)
class package(models.Model):
    id = models.IntegerField(verbose_name='id',primary_key=True)
    shelf = models.ForeignKey(shelf,on_delete=models.CASCADE, related_name="Shelf")
    shelf_compartment = models.IntegerField(blank=True,null=True,verbose_name='Compartment')
    weight = models.FloatField(blank=True,null=True)
    length = models.FloatField(blank=True,null=True)
    width = models.FloatField(blank=True,null=True)
    height = models.FloatField(blank=True,null=True)
    details = models.TextField(blank=True)
    def __str__(self):
        return str(self.id)
class hidden_package(models.Model):
    id = models.AutoField(verbose_name='id',primary_key=True)
    old_id = models.IntegerField(verbose_name='old_id')
    shelf = models.ForeignKey(shelf,on_delete=models.CASCADE, related_name="Shelff")
    shelf_compartment = models.IntegerField(blank=True,null=True,verbose_name='Compartment')
    weight = models.FloatField(blank=True,null=True)
    length = models.FloatField(blank=True,null=True)
    width = models.FloatField(blank=True,null=True)
    height = models.FloatField(blank=True,null=True)
    details = models.TextField(blank=True)
    def __str__(self):
        return str(self.old_id)
class robot(models.Model):
    name = models.CharField(max_length=120,verbose_name='Name',primary_key=True)
    height = models.FloatField(blank=True,null=True)
    length = models.FloatField(blank=True,null=True)
    width = models.FloatField(blank=True,null=True)
    status = models.BooleanField(blank=True, null=True,default=False,editable=False)
    node_id = models.ForeignKey(node,on_delete=models.CASCADE, related_name="node_id",null=True,blank=True)

class task(models.Model):
    robot = models.ForeignKey(robot,on_delete=models.CASCADE, related_name="robot")
    package = models.ForeignKey(hidden_package,on_delete=models.CASCADE, related_name="package")
    #holding_package = models.IntegerField(blank=True)
