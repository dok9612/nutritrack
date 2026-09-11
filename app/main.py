from fastapi import FastAPI, HTTPException, Query
from uuid import uuid4
from pathlib import Path

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.schemas.meal import IngredientCreate, MealCreate, MealResponse


app = FastAPI()
static_directory = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_directory), name="static")


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(static_directory / "index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


meals_content = {
    "meal_003": {
        "id": "meal_003",
        "name": "dakgalbi",
        "ingredients": [
            {"name": "chicken thigh", "grams": 150},
            {"name": "onion", "grams": 100},
        ],
    },
    "meal_004": {
        "id": "meal_004",
        "name": "bbq chicken",
        "ingredients": [
            {"name": "chicken thigh", "grams": 350},
            {"name": "onion", "grams": 50},
        ],
    },
    "meal_002": {
        "id": "meal_002",
        "name": "frozen yogurt",
        "ingredients": [
            {"name": "yogurt", "grams": 350},
            {"name": "honey", "grams": 50},
        ],
    },
    "meal_001": {
        "id": "meal_001",
        "name": "pork skewers",
        "ingredients": [
            {"name": "pork", "grams": 350},
            {"name": "garlic", "grams": 50},
            {"name": "soy sauce", "grams": 10},
        ],
    },
}


@app.get("/meals/{meals_id}")
def get_meals(meals_id: str):
    meal = meals_content.get(meals_id)

    if meal is None:
        raise HTTPException(status_code=404, detail="Meal not found")
    return meal


@app.get("/meals")
def get_all_meals(
    name: str | None = None,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
):
    meals = list(meals_content.values())
    if name is not None:
        results = []

        for meal in meals:
            if meal["name"].casefold() == name.casefold():
                results.append(meal)
        meals = results
    meals = sorted(meals, key=lambda meal: meal["id"])

    return meals[offset : offset + limit]


@app.post("/meals", status_code=201, response_model=MealResponse)
def create_meal(meal: MealCreate):
    meal_id = str(uuid4())

    record = meal.model_dump()
    record["id"] = meal_id

    meals_content[meal_id] = record
    return record
