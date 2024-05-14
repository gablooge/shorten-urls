from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from prefix_id import PrefixIDField


# Create your models here.
class User(AbstractUser):
    id = PrefixIDField(prefix="U", primary_key=True)

    def is_employee(self):
        return self.groups.filter(name="Employee").exists()

    def is_operator(self):
        return self.groups.filter(name="Operator").exists()

    def is_admin(self):
        return self.groups.filter(name="Admin").exists()


class EmployeeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(groups__name="Employee")


class Employee(User):
    objects = EmployeeManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        employee_group = Group.objects.get(name="Employee")
        self.groups.add(employee_group)
        return super().save(*args, **kwargs)


class OperatorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(groups__name="Operator")


class Operator(User):
    objects = OperatorManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        operator_group = Group.objects.get(name="Operator")
        self.groups.add(operator_group)
        return super().save(*args, **kwargs)


class AdminManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(groups__name="Admin")


class Admin(User):
    objects = AdminManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        admin_group = Group.objects.get(name="Admin")
        self.groups.add(admin_group)
        return super().save(*args, **kwargs)
