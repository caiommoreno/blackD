from datetime import datetime, timedelta, timezone

from django.conf import settings
from django.db.models import F
from schedule.models import Calendar, Event, Occurrence

EV_END_OFFSET = 15  # end offset from the event start, in minutes


def _make_aware(dt):
    return dt.replace(timezone.utc) if dt.utcoffset() is None else dt


def get_user_calendar(user):
    return Calendar.objects.get_or_create_calendar_for_object(user)


def get_occurrence(event_id, *, date=None, occurrence_id=None):
    if occurrence_id:
        return Occurrence.objects.get(id=occurrence_id)

    event = Event.objects.get(id=event_id)
    occ = event.get_occurrence(date)
    if occ is None:
        raise ValueError("Occurrence not found.")

    return occ


def cancel_occurrences(event, after_dt=None):
    date = _make_aware(after_dt or datetime.now(timezone.utc))
    event.occurrence_set.filter(start__gte=date).update(cancelled=True)
    event.end_recurring_period = date
    event.save()


def get_occurrences(event, after=None):
    start = _make_aware(after) if after else event.start
    occs_gen = event.occurrences_after(start, max_occurrences=settings.MAX_OCCURRENCES_PER_EVENT)
    not_cancelled = (occ for occ in occs_gen if not occ.cancelled)

    def past_end_period(occ):
        if not event.end_recurring_period:
            return False

        return occ.start >= event.end_recurring_period

    not_past_end = (occ for occ in not_cancelled if not past_end_period(occ))
    return not_past_end


def get_calendar_occurrences(calendar):
    events = calendar.events.all()
    occurrences = list()
    for ev in events:
        occurrences.extend(get_occurrences(ev))

    return occurrences


def create_event(calendar_slug, *, user, title, description, start):
    start = _make_aware(start)
    calendar = Calendar.objects.get(slug=calendar_slug)
    end = start + timedelta(minutes=EV_END_OFFSET)
    return Event.objects.create(
        calendar=calendar,
        title=title,
        description=description or "",
        creator=user,
        start=start,
        end=end,
    )


def update_event(event):
    event.end = event.start + timedelta(minutes=EV_END_OFFSET)
    old_event = Event.objects.get(id=event.id)
    dts = timedelta(
        minutes=int((event.start - old_event.start).total_seconds() / 60)
    )
    dte = timedelta(
        minutes=int((event.end - old_event.end).total_seconds() / 60)
    )
    event.occurrence_set.all().update(
        original_start=F("original_start") + dts,
        original_end=F("original_end") + dte,
    )
    event.save()
    return event
