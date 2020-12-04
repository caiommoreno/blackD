import pytest

from datetime import datetime, timedelta, timezone

from schedule.models import Calendar, Event, Occurrence
from blackD.core.services import (
    get_user_calendar, get_calendar_occurrences, get_occurrence, get_occurrences, cancel_occurrences,
    create_event, update_event, EV_END_OFFSET
)


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(username="user", password="user")


@pytest.fixture
def calendar(user):
    return Calendar.objects.get_or_create_calendar_for_object(user)


@pytest.fixture
def start():
    return datetime(2020, 12, 6, tzinfo=timezone.utc)


@pytest.fixture
def event(calendar, start, user):
    end = start + timedelta(minutes=15)
    return Event.objects.create(
        calendar=calendar,
        title="Test title",
        description="Test description",
        creator=user,
        start=start,
        end=end,
    )


@pytest.fixture
def occurrence(event):
    return Occurrence.objects.create(
        event=event,
        start=event.start,
        end=event.end,
        original_start=event.start,
        original_end=event.end
    )


@pytest.mark.django_db
class TestCalendar:
    def test_create_new_calendar(self, user):
        assert Calendar.objects.count() == 0
        calendar = get_user_calendar(user)
        calendars = Calendar.objects.all()
        assert len(calendars) == 1
        assert calendar == calendars.first()

    def test_get_existing_calendar(self, user):
        calendar = get_user_calendar(user)
        calendar2 = get_user_calendar(user)
        assert calendar2 == calendar

    def test_get_calendar_occurrences(self, calendar, occurrence):
        occs = get_calendar_occurrences(calendar)
        assert len(occs) == 1
        assert occs[0] == occurrence


@pytest.mark.django_db
class TestOccurrence:
    def test_get_persisted_occurrence(self, event, occurrence):
        occ = get_occurrence(event.id, occurrence_id=occurrence.id)
        assert occ == occurrence
        assert occ.id is not None

    def test_get_occurrence_by_date(self, event, start):
        occ = get_occurrence(event.id, date=start)
        assert occ.start == start
        assert occ.id is None

    @pytest.mark.usefixtures("occurrence")
    def test_get_all_event_occurrences(self, event, freezer):
        freezer.move_to(event.start)
        occs = list(get_occurrences(event))
        assert len(occs) == 1

    def test_cancel_future_occurrence(self, event, occurrence, freezer):
        freezer.move_to("2020-01-01")
        cancel_occurrences(event)
        occs = list(get_occurrences(event))
        assert len(occs) == 0

    def test_dont_cancel_past_occurrences(self, event, occurrence, freezer):
        freezer.move_to("2022-01-01")
        cancel_occurrences(event)
        occs = list(get_occurrences(event))
        assert len(occs) == 1


@pytest.mark.django_db
class TestEvent:
    def test_create_event(self, user, calendar, start):
        event = create_event(calendar.slug, user=user, title="Test title", start=start, description=None)
        assert event.start == start
        assert event.end == start + timedelta(minutes=EV_END_OFFSET)

    def test_update_event(self, event, start):
        new_start = start + timedelta(hours=10)
        event.start = new_start
        update_event(event)
        event.refresh_from_db()
        assert event.start == new_start
