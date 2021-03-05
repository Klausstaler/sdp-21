from django.db import models

# Create your models here.

class node(models.Model):
    id = models.AutoField(primary_key=True)
    first_node = models.ForeignKey('self',on_delete=models.CASCADE, related_name="first",blank=True, null=True)
    first_node_distance = models.IntegerField(verbose_name='distance_to_first',blank=True, null=True)
    second_node = models.ForeignKey('self',on_delete=models.CASCADE, related_name="second",blank=True, null=True)
    second_node_distance = models.IntegerField(verbose_name='distance_to_second',blank=True, null=True)
    third_node = models.ForeignKey('self',on_delete=models.CASCADE, related_name="third",blank=True, null=True)
    third_node_distance = models.IntegerField(verbose_name='distance_to_third',blank=True, null=True)
    fourth_node = models.ForeignKey('self',on_delete=models.CASCADE, related_name="fourth",blank=True, null=True)
    fourth_node_distance = models.IntegerField(verbose_name='distance_to_fourth',blank=True, null=True)
    fifth_node = models.ForeignKey('self',on_delete=models.CASCADE, related_name="fifth",blank=True, null=True)
    fifth_node_distance = models.IntegerField(verbose_name='distance_to_fifth',blank=True, null=True)
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
    weight = models.IntegerField(blank=True,null=True)
    length = models.IntegerField(blank=True,null=True)
    width = models.IntegerField(blank=True,null=True)
    heigth = models.IntegerField(blank=True,null=True)
    details = models.TextField(blank=True)
    def __str__(self):
        return str(self.id)
class hidden_package(models.Model):
    id = models.AutoField(verbose_name='id',primary_key=True)
    old_id = models.IntegerField(verbose_name='old_id')
    shelf = models.ForeignKey(shelf,on_delete=models.CASCADE, related_name="Shelff")
    shelf_compartment = models.IntegerField(blank=True,null=True,verbose_name='Compartment')
    weight = models.IntegerField(blank=True,null=True)
    length = models.IntegerField(blank=True,null=True)
    width = models.IntegerField(blank=True,null=True)
    heigth = models.IntegerField(blank=True,null=True)
    details = models.TextField(blank=True)
    def __str__(self):
        return str(self.old_id)
class robot(models.Model):
    name = models.CharField(max_length=120,verbose_name='Name',blank=True,null=True)
    ip = models.GenericIPAddressField(verbose_name='IP',primary_key=True)
    status = models.BooleanField(blank=True, null=True,default=False,editable=False)
    node_id = models.ForeignKey(node,on_delete=models.CASCADE, related_name="node_id",null=True,blank=True)

class task(models.Model):
    robot = models.ForeignKey(robot,on_delete=models.CASCADE, related_name="robot")
    package = models.ForeignKey(hidden_package,on_delete=models.CASCADE, related_name="package")
    holding_package = models.BooleanField(blank=True)
