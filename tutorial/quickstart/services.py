# services
from django.db import transaction
from django.contrib.auth.models import User , Group
from .tasks import send_welcome_email


@transaction.atomic
def create_user(username: str , email: str , password: str) -> User:
    user = User.objects.create_user(
        username=username,
        email=email,
        password =password
    )
    send_welcome_email.delay(user.id)
    print(f"User {user.username} created, and welcome email task has been dispatched.")
    return user




@transaction.atomic
def create_group(name: str) -> Group:
    group = Group.objects.create(name=name)
    return group

@transaction.atomic
def update_group(group: Group, name: str) -> Group:
    group.name = name
    group.save(update_fields=['name'])
    return group

@transaction.atomic
def delete_group(group: Group) -> None:
    group.delete()