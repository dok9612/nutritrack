from pydantic import BaseModel, Field, ConfigDict


class IngredientCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True, extra="forbid", allow_inf_nan=False
    )

    name: str = Field(min_length=1)
    grams: float = Field(gt=0)


class MealCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True, extra="forbid", allow_inf_nan=False
    )

    name: str = Field(min_length=1)
    ingredients: list[IngredientCreate] = Field(min_length=1)


class MealResponse(BaseModel):
    id: str
    name: str
    ingredients: list[IngredientCreate]
