from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from usom.models import User


class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    END = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def cprint(text, color=None):
    if color:
        print(color + text + Colors.END)
    else:
        print(text)


class Command(BaseCommand):
    help = "Generate initial data"

    def handle(self, *args, **kwargs):
        cprint("Hello! We are going to create a admin data.", Colors.BOLD)
        admin = User(
            first_name="Samsul",
            last_name="Hadi",
        )
        email = "samsulhadikediri@gmail.com"
        password = "samlus"
        admin.username = email
        admin.email = email
        admin.set_password(password)
        admin.save()
        admin_group = Group.objects.get(name="Admin")
        admin.groups.add(admin_group)
        print(f"Created {admin!r} for all this data!")

        employee = User.objects.create(email="employee@gmail.com")
        employee.username = "employee"
        employee.set_password("employee")
        employee.save()
        employee_group = Group.objects.get(name="Employee")
        employee.groups.add(employee_group)
        print(f"Created {employee!r} for all this data!")

        operator = User.objects.create(email="operator@gmail.com")
        operator.username = "operator"
        operator.set_password("operator")
        operator.save()
        operator_group = Group.objects.get(name="Operator")
        operator.groups.add(operator_group)
        print(f"Created {operator!r} for all this data!")
