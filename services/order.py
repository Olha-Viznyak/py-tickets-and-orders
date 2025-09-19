from typing import Optional
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket, MovieSession

User = get_user_model()


def create_order(
    tickets: list[dict],
    username: str,
    date: Optional[str] = None
) -> Order:
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise ValueError(f"User with username '{username}' does not exist")


    created_at = timezone.now()
    if date:
        try:
            created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("Date must be in format 'YYYY-MM-DD HH:MM'")

    with transaction.atomic():
        order = Order.objects.create(
            user=user,
            created_at=created_at
        )

        for ticket_info in tickets:
            movie_session = MovieSession.objects.get(id=ticket_info["movie_session"])
            Ticket.objects.create(
                order=order,
                movie_session=movie_session,
                row=ticket_info["row"],
                seat=ticket_info["seat"],
            )

    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset.order_by("-created_at")
