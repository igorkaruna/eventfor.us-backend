import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from base.tests import BaseTest
from events.models import Event
from events.tests.factories import EventFactory
from users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


class TestGetSavedEventsView(BaseTest):
    def test_get_user_with_saved_events(self, api_client: APIClient) -> None:
        # given
        user = UserFactory()
        events = [EventFactory() for _ in range(2)]
        user.profile.saved_events.add(*events)

        # then
        response = api_client.get(
            reverse(
                "user_saved_events",
                kwargs={"uuid": str(user.id)},
            )
        )

        # when
        self._common_check(response, expected_status=200)

        assert Event.objects.count() == 2, "Expected exactly 2 events in the database"

        response_data = response.json()
        assert response_data["count"] == 2, "Expected the response to contain 2 events"
