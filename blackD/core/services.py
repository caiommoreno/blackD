from datetime import datetime, timezone

from schedule.models import Calendar
from django.utils import timezone as dj_timezone


def get_user_event_occurrences(user):
    start = datetime(2020, 1, 1, tzinfo=timezone.utc)
    end = datetime(dj_timezone.now().year + 10, 12, 31, 23, 59, 59, tzinfo=timezone.utc)

    calendar = Calendar.objects.get_or_create_calendar_for_object(user)
    events = calendar.events.all()
    occurrences = list()
    for ev in events:
        occurrences.extend(ev.get_occurrences(start, end))

    return occurrences
