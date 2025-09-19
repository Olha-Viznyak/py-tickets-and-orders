from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

User = get_user_model()

def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> User:
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email or "",
        first_name=first_name or "",
        last_name=last_name or "",
    )
    return user


def get_user(user_id:int) -> User | None:
    return User.objects.filter(id=user_id).first()


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> User | None:
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return None

    with transaction.atomic():
        if username is not None:
            user.username = username
        if email is not None:
            user.email = email
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if password is not None:
            user.set_password(password)

        user.save()

    return user
