from fastapi.testclient import TestClient

from app.main import app


def test_create_and_get_meal():
    payload = {"name": "acai", "ingredients": [{"name": "strawberry", "grams": 100}]}

    with TestClient(app) as client:
        # test creation of meal
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


def test_get_missing_meal():
    with TestClient(app) as client:
        response = client.get("/meals/does-not-exist")

    assert response.status_code == 404
    assert response.json() == {"detail": "Meal not found"}
