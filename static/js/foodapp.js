// Removes flash message when a user logs in or is unable to log in
const removeFlashButton = document.getElementById("removeflash");
const elementToRemove = document.getElementById("flash");

if (removeFlashButton) { 
  removeFlashButton.addEventListener('click', (evt) => {
      evt.preventDefault();
      elementToRemove.remove();
  })
}

// Renders meals based on inputs given
 
const theMealFormButton = document.querySelector("#submit-form-button");

if (theMealFormButton){

  theMealFormButton.addEventListener('click', (evt) => {
    evt.preventDefault();
    const userCategory = document.querySelector("#category");
    const userArea  = document.querySelector("#area");
    const ingredientOne  = document.querySelector("#ingredient1");
    const ingredientTwo = document.querySelector("#ingredient2");
    const ingredientThree = document.querySelector("#ingredient3");

    const queryString = `?category=${userCategory.value}&area=${userArea.value}&ingredient1=${ingredientOne.value}&ingredient2=${ingredientTwo.value}&ingredient3=${ingredientThree.value}`;
    
    fetch(`/api/meals${queryString}`)
      .then((response) => response.json())
      .then((data) => {
        const mealsDiv = document.querySelector("#returned-meals");
        mealsDiv.innerHTML = "";
        data.meals.forEach((meal) => {
          const mealDiv = document.createElement("div");
          mealDiv.classList.add("meal-item");
          mealDiv.innerHTML = `
            <h4>${meal.name}</h4>
            <p>Category: ${meal.category}</p>
            <p>Area: ${meal.area}</p>
            <img src="${meal.image}" alt="${meal.name}" class="mini-meal" />
            <a href="/recipe/${meal.name}/${meal.id}">
              <button class = "button"> Explore Meal </button> 
            </a>
          `;
          mealsDiv.appendChild(mealDiv);
        });
      });
  })
}