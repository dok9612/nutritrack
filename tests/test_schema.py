import pytest
from pydantic import ValidationError

from app.schemas.meal import IngredientCreate, MealCreate

payload = {"name": "acai", "ingredients": [{"name": "strawberry", "grams": 150}]}


def test_valid_meal_builds_nested_ingredients():
    meal = MealCreate(**payload)

    meal_dict = meal.model_dump()

    assert meal.name == "acai"
    assert isinstance(meal.ingredients[0], IngredientCreate)
    assert meal.ingredients[0].name == "strawberry"
    assert meal.ingredients[0].grams == 150
    assert meal_dict["name"] == "acai"
    assert meal_dict == payload


def test_meal_rejects_empty_name():
    with pytest.raises(ValidationError):
        MealCreate(
            name="",
            ingredients=[IngredientCreate(name="strawberry", grams=150)],
        )


def test_meal_requires_name():
    with pytest.raises(ValidationError):
        MealCreate(
            ingredients=[IngredientCreate(name="strawberry", grams=150)],
        )


def test_meal_rejects_empty_ingredient_name():
    with pytest.raises(ValidationError):
        MealCreate(
            name="acai",
            ingredients=[IngredientCreate(name="", grams=150)],
        )


def test_meal_requires_ingredient_name():
    with pytest.raises(ValidationError):
        MealCreate(
            name="acai",
            ingredients=[IngredientCreate(grams=150)],
        )


def test_meal_rejects_empty_ingredient_list():
    with pytest.raises(ValidationError):
        MealCreate(
            name="acai",
            ingredients=[],
        )


def test_meal_requires_ingredient_list():
    with pytest.raises(ValidationError):
        MealCreate(
            name="acai",
        )


def test_ingredient_accepts_small_positive_weight():
    ingredient = IngredientCreate(
        name="strawberry",
        grams=0.1,
    )

    assert ingredient.grams == 0.1


def test_meal_trims_pads():
    meal = MealCreate(
        name=" strawberry bowl ",
        ingredients=[IngredientCreate(name="strawberry", grams=100)],
    )

    assert meal.name == "strawberry bowl"


def test_ingredient_trims_pads():
    ingredient = IngredientCreate(name="  blueberries ", grams=100)

    assert ingredient.name == "blueberries"


def test_meal_reject_whitespace_only():
    with pytest.raises(ValidationError):
        MealCreate(
            name="   ",
            ingredients=[IngredientCreate(name="strawberry", grams=100)],
        )


def test_ingredient_reject_whitespace_only():
    with pytest.raises(ValidationError):
        IngredientCreate(name="   ", grams=100)


@pytest.mark.parametrize("grams", [-50, 0])
def test_ingredient_rejects_nonpositive_grams(grams):
    with pytest.raises(ValidationError):
        IngredientCreate(name="strawberry", grams=grams)


def test_ingredient_requires_grams():
    with pytest.raises(ValidationError):
        IngredientCreate(name="strawberry")


@pytest.mark.parametrize("grams", [float("inf"), float("-inf"), float("nan")])
def test_ingredient_reject_nonfinite_grams(grams):
    with pytest.raises(ValidationError):
        IngredientCreate(name="strawberry", grams=grams)


def test_ingredient_rejects_unknown_field():
    with pytest.raises(ValidationError):
        IngredientCreate(name="berry", grams=100, unexpected="unexpected_str")


def test_meal_rejects_unknown_field():
    with pytest.raises(ValidationError):
        MealCreate(
            name="acai bowl",
            ingredients=[IngredientCreate(name="berry", grams=100)],
            unexpected="unexpected_str",
        )


def test_ingredient_accepts_numeric_string():
    ingredient = IngredientCreate(name="berry", grams="150")

    assert ingredient.grams == 150
    assert isinstance(ingredient.grams, float)


def test_meal_rejects_client_supplied_ids():
    with pytest.raises(ValidationError):
        meal = MealCreate(
            name="acai bowl",
            ingredients=[IngredientCreate(name="berry", grams=100)],
            id=1234,
        )
