from django.contrib.auth.models import User , Group


def list_users():
    return User.objects.all()



def get_user_by_id(user_id: int):
    return User.objects.get(id=user_id)


def list_groups():
    return Group.objects.all()

def get_group_by_id(group_id: int) -> Group:
    return Group.objects.get(id=group_id)

