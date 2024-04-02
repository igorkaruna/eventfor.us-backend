from datetime import datetime, timedelta

import freezegun
import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from base.tests import BaseTest
from events.constants import EventAttendanceIntent, EventSaveAction
from events.models import Event
from events.repositories import EventAttendanceRepository
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

    @pytest.mark.parametrize(
        "invalid_capacity, expected_error_message",
        [
            (-1, ["Ensure this value is greater than or equal to 0."]),
            (100_000, ["Ensure this value is less than or equal to 10000."]),
        ],
    )
    def test__create_event__invalid_capacity__failed(
        self, api_client: APIClient, invalid_capacity: str, expected_error_message: list[str]
    ) -> None:
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
                    "capacity": invalid_capacity,
                    "description": "Test description",
                    "start_date": (datetime.now() + timedelta(days=1)).date().isoformat(),
                    "end_date": (datetime.now() + timedelta(days=2)).date().isoformat(),
                },
            )

        # then
        self._common_check(response, expected_status=400)

        response_data = response.json()
        assert response_data["capacity"] == expected_error_message

    def test__create_event_invalid_start_date__failed(self, api_client: APIClient) -> None:
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
                    "start_date": (datetime.now() + timedelta(days=3)).date().isoformat(),
                    "end_date": (datetime.now() + timedelta(days=2)).date().isoformat(),
                },
            )

        # then
        self._common_check(response, expected_status=400)

        response_data = response.json()
        assert response_data["start_date"] == ["The start date must be before the end date."]

    def test__list_events__success(self, api_client: APIClient) -> None:
        # given
        events = [EventFactory() for _ in range(5)]

        # when
        response = api_client.get(self.endpoint)

        # then
        self._common_check(response)

        response_data = response.json()["results"]
        assert len(response_data) == len(events), "The number of events does not match the expected count"

    def test__retrieve_event__success(self, api_client: APIClient) -> None:
        # given
        event = EventFactory()

        # when
        response = api_client.get(
            reverse(
                "event-detail",
                args=[str(event.id)],
            )
        )

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

    def test__delete_event_by_creator__success(self, api_client: APIClient) -> None:
        # given
        creator = UserFactory()
        event = EventFactory(creator=creator)

        # when
        api_client.force_authenticate(creator)

        response = api_client.delete(
            reverse(
                "event-detail",
                args=[str(event.id)],
            )
        )

        # then
        self._common_check(
            response,
            expected_status=204,
            expected_content_type=None,
        )

        assert Event.objects.count() == 0

    def test__delete_event_not_by_creator__faile(self, api_client: APIClient) -> None:
        # given
        creator = UserFactory()
        event = EventFactory(creator=creator)

        guest = UserFactory()
        api_client.force_authenticate(guest)

        # when
        response = api_client.delete(
            reverse(
                "event-detail",
                args=[str(event.id)],
            )
        )

        # then
        self._common_check(response, expected_status=403)

        assert Event.objects.count() == 1

        response_data = response.json()
        assert response_data["detail"] == "You do not have permission to perform this action."

    def test__attend_event__authenticated_user__success(self, api_client: APIClient) -> None:
        # given
        user = UserFactory()
        event = EventFactory()

        # when attend
        api_client.force_authenticate(user)

        response_attend = api_client.post(
            reverse(
                "event-attend",
                args=[str(event.id)],
            )
        )

        # then
        self._common_check(response_attend)

        response_data_attend = response_attend.json()
        assert response_data_attend["detail"] == f"Attendance {EventAttendanceIntent.Reserved.lower()}."

        assert EventAttendanceRepository.is_user_attending_event(
            user=user,
            event=event,
        ), "User should be marked as attending the event"

        # when cancel reservation
        response_cancel = api_client.post(
            reverse(
                "event-attend",
                args=[str(event.id)],
            )
        )

        # then
        self._common_check(response_cancel)

        assert not EventAttendanceRepository.is_user_attending_event(
            user=user,
            event=event,
        ), "User should no longer be marked as attending the event"

        response_data_cancel = response_cancel.json()
        assert response_data_cancel["detail"] == f"Attendance {EventAttendanceIntent.Canceled.lower()}."

    def test__event_not_open_for_attendance__failed(self, api_client: APIClient):
        # given
        user = UserFactory()
        event = EventFactory(
            start_date=timezone.now() - timedelta(days=2),
            end_date=timezone.now() - timedelta(days=1),
        )

        # when
        api_client.force_authenticate(user)
        response = api_client.post(
            reverse(
                "event-attend",
                args=[str(event.id)],
            )
        )

        # then
        self._common_check(response, expected_status=400)

        response_data = response.json()
        assert response_data["detail"] == "The event is not open for attendance."

    def test__toggle_save_event__authenticated_user__success(self, api_client: APIClient) -> None:
        # given
        user = UserFactory()
        event = EventFactory()

        # when toggle save
        api_client.force_authenticate(user)

        response_save = api_client.post(
            reverse(
                "event-toggle-save",
                args=[str(event.id)],
            )
        )

        # then
        self._common_check(response_save)

        user.refresh_from_db()
        assert user.profile.saved_events.count() == 1, "Expected one event to be saved"

        response_data_save = response_save.json()
        assert response_data_save["detail"] == f"Event {EventSaveAction.Saved.lower()} successfully."

        # when toggle unsave
        response_unsave = api_client.post(
            reverse(
                "event-toggle-save",
                args=[str(event.id)],
            )
        )

        # then
        self._common_check(response_unsave)

        user.refresh_from_db()
        assert user.profile.saved_events.count() == 0, "Expected no events to be saved after untoggling"

        response_data_unsave = response_unsave.json()
        assert response_data_unsave["detail"] == f"Event {EventSaveAction.Removed.lower()} successfully."

    def test__toggle_save_event__unauthenticated_user__failed(self, api_client: APIClient) -> None:
        # given
        event = EventFactory()

        # when
        response = api_client.post(reverse("event-toggle-save", args=[str(event.id)]))

        # then
        self._common_check(response, expected_status=401)

        response_data = response.json()
        assert response_data["detail"] == "Authentication credentials were not provided."
