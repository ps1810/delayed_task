import json

from fastapi import status
from fastapi.testclient import TestClient
from .helpers import generators

shared_data = {}
# client = TestClient(app)

def test_post_task(client: TestClient) -> None:
    """
    To test the creation of task
    :param client:
    :return:
    """
    test_input = generators.create_valid_timer_request()
    response = client.post(
        "/api/v1/timer",
        json=test_input
    )
    print(response.json(), flush=True)
    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()

    shared_data["id"] = response_data["id"]
    assert response_data["time_left"] == 3661


def test_get_task(client: TestClient) -> None:
    """
    To test the /timer/<task_id> API. It should return the same task id with time_left
    :param client:
    :return:
    """
    response = client.get(
        f"/api/v1/timer/{shared_data['id']}"
    )
    assert response.status_code == status.HTTP_200_OK

    get_response = response.json()
    assert shared_data['id'] == get_response["id"]
    assert "time_left" in get_response


def test_post_task_with_wrong_url(client: TestClient) -> None:
    """
    To test if request validation works by sending invalid url
    :param client:
    :return:
    """
    test_input = generators.create_invalid_url_timer_request()
    response = client.post(
        "/api/v1/timer",
        json=test_input
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response_data = response.json()
    assert response_data["detail"] == "Invalid URL"
