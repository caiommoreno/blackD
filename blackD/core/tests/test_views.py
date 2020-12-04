import json
from datetime import datetime, timezone, timedelta

import pytest
from dateutil.parser import parse as dt_parse

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from schedule.models import Event
from blackD.core.services import get_user_calendar, get_occurrences

User = get_user_model()

pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def auth_user(client):
    user = User.objects.create(username="user")
    client.force_login(user)
    return user


@pytest.fixture
def calendar(auth_user):
    return get_user_calendar(auth_user)


class TestCreateEventView:
    def url(self):
        return reverse("event-list")

    @pytest.fixture(autouse=True)
    def auth_user(self, client, auth_user):
        self.auth_user = auth_user
        return self.auth_user

    @pytest.fixture(autouse=True)
    def calendar(self, calendar):
        self.calendar = calendar
        return calendar

    @pytest.fixture
    def data(self):
        return {
            "title": "Test event",
            "start": "2020-12-19T07:20",
            "tzoffset": 180,
        }

    def test_create_event_success(self, client, data):
        assert Event.objects.count() == 0
        res = client.post(self.url(), data=data)
        events = list(Event.objects.all())
        assert res.status_code == 201
        assert len(events) == 1

        expected_start = datetime.fromisoformat("2020-12-19T10:20:00+00:00")
        expected_end = datetime.fromisoformat("2020-12-19T10:35:00+00:00")

        assert res.data.get("id") is not None
        assert dt_parse(res.data["start"]) == expected_start
        assert dt_parse(res.data["end"]) == expected_end
        assert res.data["title"] == data["title"]

    def test_unauthenticated_user_forbidden(self, client, data):
        client.logout()
        res = client.post(self.url(), data=data)
        assert res.status_code == 403


class TestUpdateEventView:
    def url(self, event_id):
        return reverse("event-detail", kwargs={"id": event_id})

    @pytest.fixture(autouse=True)
    def auth_user(self, client, auth_user):
        self.auth_user = auth_user
        return self.auth_user

    @pytest.fixture(autouse=True)
    def calendar(self, calendar):
        self.calendar = calendar
        return calendar

    @pytest.fixture
    def start(self):
        return datetime(2020, 12, 6, tzinfo=timezone.utc)

    @pytest.fixture
    def event(self, calendar, start, auth_user):
        end = start + timedelta(minutes=15)
        return Event.objects.create(
            calendar=calendar,
            title="Test title",
            description="Test description",
            creator=auth_user,
            start=start,
            end=end,
        )

    def test_update_event(self, client, event):
        data = {
            "title": "Test event",
            "start": "2020-12-26T07:00",
            "tzoffset": 180,
        }

        res = client.put(self.url(event.id), data=data)
        assert res.status_code == 200
        assert res.data["start"] == "2020-12-26T10:00:00Z"
        assert res.data["end"] == "2020-12-26T10:15:00Z"


class TestCancelOccurrencesView:
    def url(self, event_id):
        return reverse("event-cancel-occurrences", kwargs={"id": event_id})

    @pytest.fixture(autouse=True)
    def auth_user(self, client, auth_user):
        self.auth_user = auth_user
        return self.auth_user

    @pytest.fixture
    def start(self):
        return datetime(2020, 12, 6, tzinfo=timezone.utc)

    @pytest.fixture
    def event(self, calendar, start, auth_user):
        end = start + timedelta(minutes=15)
        return Event.objects.create(
            calendar=calendar,
            title="Test title",
            description="Test description",
            creator=auth_user,
            start=start,
            end=end,
        )

    def test_cancel_all_occurrences(self, client, event, freezer):
        freezer.move_to("2020-01-01")
        res = client.post(self.url(event.id))
        assert res.status_code == 200
        event.refresh_from_db()
        occs = list(get_occurrences(event))
        assert not occs

    def test_cancel_occurrences_after_date(self, client, event, freezer):
        freezer.move_to("2020-01-01")
        data = {"after_dt": datetime.now(timezone.utc).isoformat()}
        res = client.post(self.url(event.id), data=data)
        assert res.status_code == 200
        event.refresh_from_db()
        occs = list(get_occurrences(event))
        assert not occs
