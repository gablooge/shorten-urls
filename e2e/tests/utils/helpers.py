from usom.models import User


def createSuperUser():
    user = User.objects.create_user(
        "super_user", "super_admin@gmail.com", "sangatrahasia"
    )
    user.is_active = True
    user.is_staff = True
    user.is_superuser = True
    user.save()
    return user
