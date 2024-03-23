import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from base.tests import BaseTest
from events.tests.factories import EventCategoryFactory, EventFactory
from users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


class TestEventFilter(BaseTest):
    endpoint = reverse("event-list")

    def test_filter_by_category(self, api_client: APIClient) -> None:
        # given
        sports_category = EventCategoryFactory(name="Sports")
        networking_category = EventCategoryFactory(name="Networking")

        for category in {sports_category, networking_category}:
            EventFactory(category=category)

        # when
        response = api_client.get(
            self.endpoint,
            {"category": sports_category.id},
        )

        # then
        self._common_check(response)

        response_data = response.json()["results"]
        assert len(response_data) == 1, f"Expected only one event in category: {sports_category.name}"

    def test_filter_by_creator(self, api_client: APIClient) -> None:
        # given
        creator_john = UserFactory(first_name="John")
        creator_emily = UserFactory(first_name="Emily")

        for creator in {creator_john, creator_emily}:
            EventFactory(creator=creator)

        # when
        response = api_client.get(
            self.endpoint,
            {"creator": creator_john.id},
        )

        # then
        self._common_check(response)

        response_data = response.json()["results"]
        assert len(response_data) == 1, f"Expected only one event created by {creator_john.first_name}"

    def test_filter_by_location_contains(self, api_client: APIClient) -> None:
        # given
        for location in {"Paris, France", "Los Angeles, USA", "New York, USA"}:
            EventFactory(location=location)

        # when
        response = api_client.get(
            self.endpoint,
            {"location": "USA"},
        )

        # then
        self._common_check(response)

        response_data = response.json()["results"]
        assert len(response_data) == 2, "Expected two events with location 'USA'"

    def test_filter_by_start_date_gte(self, api_client: APIClient) -> None:
        # given
        for start_date in {"2024-07-27", "2024-08-28"}:
            EventFactory(start_date=start_date)

        # when
        response = api_client.get(
            self.endpoint,
            {"start_date_gte": "2024-08-28"},
        )

        # then
        self._common_check(response)

        response_data = response.json()["results"]
        assert len(response_data) == 1, "Expected only one event with start_date >= '2024-08-28'"
