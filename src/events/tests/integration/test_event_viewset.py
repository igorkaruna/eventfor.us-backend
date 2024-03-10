from datetime import datetime, timedelta

import freezegun
import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from base.tests import BaseTest
from events.constants import SaveEventConstant
from events.models import Event
from events.tests.factories import EventCategoryFactory, EventFactory
from users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


class TestEvent(BaseTest):
    endpoint = reverse("event-list")

    def test__create_event__success(self, api_client: APIClient) -> None:
        # given
        user = UserFactory()
        event_category = EventCategoryFactory()

        # when
        api_client.force_authenticate(user)

        with freezegun.freeze_time(datetime(2024, 5, 19, 16, 45)):
            response = api_client.post(
                self.endpoint,
                data={
                    "category": str(event_category.id),
                    "name": "Test event",
                    "location": "Test location",
                    "capacity": 100,
                    "description": "Test description",
                    "start_date": (datetime.now() + timedelta(days=1)).date().isoformat(),
                    "end_date": (datetime.now() + timedelta(days=2)).date().isoformat(),
                },
            )

        # then
        self._common_check(response, expected_status=201)

        assert Event.objects.count() == 1, "The event should be created"

        response_data = response.json()

        creator = response_data["creator"]
        assert creator["id"] == str(user.id), "The creator ID does not match the authenticated user's ID"
        assert creator["email"] == str(user.email)
        assert creator["first_name"] == str(user.first_name)
        assert creator["last_name"] == str(user.last_name)

        category = response_data["category"]
        assert category["id"] == str(event_category.id)
        assert category["name"] == event_category.name
        assert category["description"] == event_category.description

        assert response_data["name"] == "Test event"
        assert response_data["location"] == "Test location"
        assert response_data["description"] == "Test description"
        assert response_data["capacity"] == 100
        assert response_data["start_date"] == "2024-05-20"
        assert response_data["end_date"] == "2024-05-21"

    def test__unauthenticated_user_create_event__failed(self, api_client: APIClient) -> None:
        # given
        event_category = EventCategoryFactory()

        # when
        with freezegun.freeze_time(datetime(2024, 5, 19, 16, 45)):
            response = api_client.post(
                self.endpoint,
                data={
                    "category": str(event_category.id),
                    "name": "Test event",
                    "location": "Test location",
                    "capacity": 100,
                    "description": "Test description",
                    "start_date": (datetime.now() + timedelta(days=1)).date().isoformat(),
                    "end_date": (datetime.now() + timedelta(days=2)).date().isoformat(),
                },
            )

        # then
        self._common_check(response, expected_status=401)

        response_data = response.json()
        assert response_data["detail"] == "Authentication credentials were not provided."

    def test__list_events__success(self, api_client: APIClient) -> None:
        # given
        events = [EventFactory() for _ in range(5)]

        # when
        response = api_client.get(self.endpoint)

        # then
        self._common_check(response)

        response_data = response.json()
        assert len(response_data) == len(events), "The number of events does not match the expected count"

    def test__retrieve_event__success(self, api_client: APIClient) -> None:
        # given
        event = EventFactory()

        # when
        response = api_client.get(reverse("event-detail", args=[str(event.id)]))

        # then
        self._common_check(response)

        response_data = response.json()
        assert response_data["id"] == str(event.id)

    def test__update_event_by_creator__success(self, api_client: APIClient) -> None:
        # given
        creator = UserFactory()
        event = EventFactory(creator=creator)

        # when
        api_client.force_authenticate(creator)

        response = api_client.patch(
            reverse("event-detail", args=[str(event.id)]),
            data={
                "name": "Updated event name",
            },
        )

        # then
        self._common_check(response)

        response_data = response.json()
        assert response_data["id"] == str(event.id)
        assert response_data["name"] == "Updated event name"

    def test__update_event_not_by_creator__failed(self, api_client: APIClient) -> None:
        # given
        guest = UserFactory()
        creator = UserFactory()
        event = EventFactory(creator=creator)

        # when
        api_client.force_authenticate(guest)

        response = api_client.patch(
            reverse("event-detail", args=[str(event.id)]),
            data={
                "name": "Updated event name",
            },
        )

        # then
        self._common_check(response, expected_status=403)

        event.refresh_from_db()
        assert event.name != "Updated event name", "Event name should not be changed"

        response_data = response.json()
        assert response_data["detail"] == "You do not have permission to perform this action."

    def test_delete_event_by_creator(self, api_client: APIClient) -> None:
        # given
        creator = UserFactory()
        event = EventFactory(creator=creator)

        # when
        api_client.force_authenticate(creator)

        response = api_client.delete(reverse("event-detail", args=[str(event.id)]))

        # then
        self._common_check(
            response,
            expected_status=204,
            expected_content_type=None,
        )

        assert Event.objects.count() == 0

    def test_delete_event_not_by_creator(self, api_client: APIClient) -> None:
        # given
        creator = UserFactory()
        event = EventFactory(creator=creator)

        guest = UserFactory()
        api_client.force_authenticate(guest)

        # when
        response = api_client.delete(reverse("event-detail", args=[str(event.id)]))

        # then
        self._common_check(response, expected_status=403)

        assert Event.objects.count() == 1

        response_data = response.json()
        assert response_data["detail"] == "You do not have permission to perform this action."

    def test_toggle_save_event__authenticated_user__success(self, api_client: APIClient) -> None:
        # given
        user = UserFactory()
        event = EventFactory()

        # when
        api_client.force_authenticate(user)

        response = api_client.post(reverse("event-toggle-save", args=[str(event.id)]))

        # then
        self._common_check(response)

        user.refresh_from_db()
        assert user.profile.saved_events.count() == 1, "Expected one event to be saved"

        response_data = response.json()
        assert response_data["event_id"] == str(event.id)
        assert response_data["action"] in {SaveEventConstant.Saved, SaveEventConstant.Removed}

    def test_toggle_save_event__unauthenticated_user__failed(self, api_client: APIClient) -> None:
        # given
        event = EventFactory()

        # when
        response = api_client.post(reverse("event-toggle-save", args=[str(event.id)]))

        # then
        self._common_check(response, expected_status=401)

        response_data = response.json()
        assert response_data["detail"] == "Authentication credentials were not provided."
