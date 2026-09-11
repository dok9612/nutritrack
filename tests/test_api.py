from copy import deepcopy
from fastapi.testclient import TestClient
import pytest

from app.main import app, meals_content


@pytest.fixture
def client():
    snapshot = deepcopy(meals_content)

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        meals_content.clear()
        meals_content.update(snapshot)


@pytest.fixture
def valid_payload():
    return {
        "name": "Oatmeal",
        "ingredients": [{"name": "Oats", "grams": 50}],
    }


INVALID_PAYLOADS = {
    "zero-grams": {
        "name": "Oatmeal",
        "ingredients": [{"name": "Oats", "grams": 0}],
    },
    "negative-grams": {
        "name": "Oatmeal",
        "ingredients": [{"name": "Oats", "grams": -50}],
    },
    "missing-meal-name": {
        "ingredients": [{"name": "Oats", "grams": 50}],
    },
    "empty-meal-name": {
        "name": "",
        "ingredients": [{"name": "Oats", "grams": 50}],
    },
    "blank-meal-name": {
        "name": "   ",
        "ingredients": [{"name": "Oats", "grams": 50}],
    },
    "missing-ingredient-name": {
        "name": "Oatmeal",
        "ingredients": [{"grams": 50}],
    },
    "empty-ingredient-name": {
        "name": "Oatmeal",
        "ingredients": [{"name": "", "grams": 50}],
    },
    "blank-ingredient-name": {
        "name": "Oatmeal",
        "ingredients": [{"name": "   ", "grams": 50}],
    },
    "missing-grams": {
        "name": "Oatmeal",
        "ingredients": [{"name": "Oats"}],
    },
    "missing-ingredients": {
        "name": "Oatmeal",
    },
    "empty-ingredients": {
        "name": "Oatmeal",
        "ingredients": [],
    },
    "unknown-meal-field": {
        "name": "Oatmeal",
        "ingredients": [{"name": "Oats", "grams": 50}],
        "unexpected": "value",
    },
    "unknown-ingredient-field": {
        "name": "Oatmeal",
        "ingredients": [{"name": "Oats", "grams": 50, "unexpected": "value"}],
    },
    "client-supplied-id": {
        "name": "Oatmeal",
        "ingredients": [{"name": "Oats", "grams": 50}],
        "id": "11111111-1111-4111-8111-111111111111",
    },
}


@pytest.fixture
def invalid_payloads():
    return deepcopy(INVALID_PAYLOADS)


@pytest.fixture
def nonfinite_payloads():
    # Direct schema tests only: inf and nan are not standard JSON numbers.
    return {
        "positive-infinity": {
            "name": "Oatmeal",
            "ingredients": [{"name": "Oats", "grams": float("inf")}],
        },
        "negative-infinity": {
            "name": "Oatmeal",
            "ingredients": [{"name": "Oats", "grams": float("-inf")}],
        },
        "nan": {
            "name": "Oatmeal",
            "ingredients": [{"name": "Oats", "grams": float("nan")}],
        },
    }


def test_create_and_get_meal(client, valid_payload):
    # test creation of meal
    payload = valid_payload
    create_response = client.post("/meals", json=payload)

    assert create_response.status_code == 201

    created = create_response.json()

    assert created["name"] == payload["name"]
    assert created["ingredients"] == payload["ingredients"]

    # test retrieval of specific meal
    meal_id = created["id"]
    get_response = client.get(f"/meals/{meal_id}")

    assert get_response.status_code == 200
    assert get_response.json() == created

    list_response = client.get("/meals")

    assert list_response.status_code == 200
    assert created in list_response.json()


def test_distinct_ids(client, valid_payload):
    payload = valid_payload
    response_1 = client.post("/meals", json=payload)
    response_2 = client.post("/meals", json=payload)

    assert response_1.status_code == 201
    assert response_2.status_code == 201

    created_1 = response_1.json()
    created_2 = response_2.json()

    assert created_1["id"] != created_2["id"]

    saved_1 = client.get(f"/meals/{created_1['id']}").json()
    saved_2 = client.get(f"/meals/{created_2['id']}").json()

    assert saved_1 == created_1
    assert saved_2 == created_2

    saved_list = client.get("/meals").json()

    assert saved_1["id"] != saved_2["id"]
    assert saved_1 in saved_list
    assert saved_2 in saved_list


def test_get_missing_meal(client):

    response = client.get("/meals/does-not-exist")

    assert response.status_code == 404
    assert response.json() == {"detail": "Meal not found"}


def test_trimmed_names_stored(client, valid_payload):
    payload = valid_payload
    payload["name"] = "  acai      "
    payload["ingredients"][0]["name"] = "  strawberry      "

    response = client.post("/meals", json=payload)
    assert response.status_code == 201

    created = response.json()
    assert created["name"] == "acai"
    assert created["ingredients"][0]["name"] == "strawberry"

    saved = client.get(f"/meals/{created['id']}")
    assert saved.status_code == 200
    assert saved.json() == created


@pytest.mark.parametrize("case_name", list(INVALID_PAYLOADS))
def test_unchanged_list_from_invalid_inputs(client, invalid_payloads, case_name):
    payload = invalid_payloads[case_name]
    before = client.get("/meals").json()
    response = client.post("/meals", json=payload)
    after = client.get("/meals").json()

    assert before == after
    assert response.status_code == 422


def test_valid_response(client, valid_payload):
    payload = valid_payload

    response = client.post("/meals", json=payload)
    saved = response.json()

    assert set(saved.keys()) == {"id", "name", "ingredients"}


def test_returns_nonempty_id(client, valid_payload):
    response = client.post("/meals", json=valid_payload)
    created = response.json()

    assert isinstance(created["id"], str)
    assert created["id"]


def test_sorted_meals(client):
    response = client.get("/meals")
    assert response.status_code == 200

    meals = response.json()

    ids = [meal["id"] for meal in meals]

    assert ids == [
        "meal_001",
        "meal_002",
        "meal_003",
        "meal_004",
    ]


def test_name_filter_is_case_insensitive(client):
    response = client.get("/meals", params={"name": "dAkGAlBi"})

    assert response.status_code == 200

    meals = response.json()

    assert len(meals) == 1
    assert meals[0]["name"] == "dakgalbi"


def test_name_filter_requires_exact_match(client):
    response = client.get("/meals", params={"name": "dak"})

    assert response.status_code == 200
    assert response.json() == []


def test_returns_empty_list_when_no_match_found(client):
    response = client.get("/meals", params={"name": "not-found"})

    assert response.status_code == 200

    meals = response.json()

    assert meals == []


def test_adjacent_pages_do_not_overlap(client):
    response_1 = client.get("/meals", params={"offset": 0, "limit": 2})
    response_2 = client.get("/meals", params={"offset": 2, "limit": 2})

    assert response_1.status_code == 200
    assert response_2.status_code == 200

    meals_1 = response_1.json()
    meals_2 = response_2.json()

    ids_1 = [meal["id"] for meal in meals_1]
    ids_2 = [meal["id"] for meal in meals_2]

    assert ids_1 == ["meal_001", "meal_002"]
    assert ids_2 == ["meal_003", "meal_004"]
    assert set(ids_1).isdisjoint(ids_2)


@pytest.mark.parametrize(
    "params", [{"offset": -1}, {"limit": 0}, {"limit": 101}, {"limit": -99}]
)
def test_reject_invalid_inputs_for_offset_limit(client, params):
    response = client.get("/meals", params=params)

    assert response.status_code == 422
