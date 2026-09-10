const form = document.querySelector("#meal-form");
const saveButton = document.querySelector("#save-button");
const refreshButton = document.querySelector("#refresh-button");
const saveStatus = document.querySelector("#save-status");
const listStatus = document.querySelector("#list-status");
const mealList = document.querySelector("#meal-list");
const mealCount = document.querySelector("#meal-count");

function showStatus(element, message, isError = false) {
  element.textContent = message;
  element.dataset.error = String(isError);
}

// Build elements with textContent so meal names are displayed as text, never HTML.
function renderMeals(meals) {
  const cards = meals.slice().reverse().map((meal) => {
    const card = document.createElement("li");
    card.className = "meal-card";
    const heading = document.createElement("h3");
    heading.textContent = meal.name;
    const ingredients = document.createElement("ul");
    ingredients.className = "ingredients";

    for (const ingredient of meal.ingredients) {
      const row = document.createElement("li");
      const name = document.createElement("span");
      name.textContent = ingredient.name;
      const weight = document.createElement("span");
      weight.className = "weight";
      weight.textContent = `${ingredient.grams} g`;
      row.append(name, weight);
      ingredients.append(row);
    }

    card.append(heading, ingredients);
    return card;
  });

  mealList.replaceChildren(...cards);
  mealCount.textContent = String(meals.length);
}

async function loadMeals() {
  refreshButton.disabled = true;
  showStatus(listStatus, "Loading meals…");
  try {
    const response = await fetch("/meals");
    if (!response.ok) throw new Error("Could not load meals.");
    const meals = await response.json();
    renderMeals(meals);
    showStatus(listStatus, meals.length ? "" : "No meals yet. Add your first meal.");
  } catch (error) {
    showStatus(listStatus, "Could not refresh meals. Check that the server is running, then press Refresh.", true);
  } finally {
    refreshButton.disabled = false;
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const name = form.elements["meal-name"].value.trim();
  const ingredientName = form.elements["ingredient-name"].value.trim();
  const grams = Number(form.elements.grams.value);

  if (!name || !ingredientName || !Number.isFinite(grams) || grams <= 0) {
    showStatus(saveStatus, "Enter both names and an amount greater than zero.", true);
    return;
  }

  // This is the same JSON body you sent with TestClient in your Python tests.
  const payload = { name, ingredients: [{ name: ingredientName, grams }] };
  saveButton.disabled = true;
  showStatus(saveStatus, "Saving meal…");

  try {
    const response = await fetch("/meals", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      showStatus(saveStatus, "The meal was not saved. Check your entries and try again.", true);
      return;
    }
    form.reset();
    showStatus(saveStatus, `${name} saved.`);
    await loadMeals();
    form.elements["meal-name"].focus();
  } catch (error) {
    showStatus(saveStatus, "Could not confirm the save. Refresh the meal list before trying again.", true);
  } finally {
    saveButton.disabled = false;
  }
});

refreshButton.addEventListener("click", loadMeals);
loadMeals();
