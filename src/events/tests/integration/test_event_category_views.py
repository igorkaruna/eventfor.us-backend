import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from base.tests import BaseTest
from events.tests.factories import EventCategoryFactory


pytestmark = pytest.mark.django_db


class TestListEventCategoryView(BaseTest):
    endpoint = reverse("categories_list")

    def test_list_categories_success(self, api_client: APIClient) -> None:
        # given
        categories = [EventCategoryFactory(name=f"Category {number}") for number in range(5)]

        # when
        response = api_client.get(self.endpoint)

        # then
        self._common_check(response)

        response_data = response.json()
        assert response_data["count"] == len(categories), "The count of categories does not match"
        assert len(response_data["results"]) == len(categories), "The results count of categories does not match"

    def test_list_categories_empty(self, api_client: APIClient) -> None:
        # when
        response = api_client.get(self.endpoint)

        # then
        self._common_check(response)

        response_data = response.json()
        assert response_data["count"] == 0, "Expected no categories to be returned"
