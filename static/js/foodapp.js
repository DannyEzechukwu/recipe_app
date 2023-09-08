// Removes all flash messages

const removeFlashButton = document.getElementById("removeflash");
const elementToRemove = document.getElementById("flash");

if (removeFlashButton) { 
  removeFlashButton.addEventListener('click', (evt) => {
      evt.preventDefault();
      elementToRemove.remove();
  })
}

// Renders meals based on inputs given on meal_details_poage
 
const theMealFormButton = document.querySelector("#submit-options-for-meal-button");

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
            <br>
            <a href="/recipe/${meal.name}/${meal.id}">
              <button class = "button"> Explore Meal </button> 
            </a>
          `;
          mealsDiv.appendChild(mealDiv);
        });
      });
  })
}


//Include or Remove ingredients for the meal being added on the add_a_meal page
const ingredientAdderButton = document.getElementById("ingredient-adder");
const ingredientRemoverButton = document.getElementById('ingredient-remover');
const addedIngredientsSection = document.getElementById("ingredients");
// unique identifier for id and name for ingredient elements
let idIncrementer = 1;
// incrementer to keep number of ingredients added to no more than 12 


if (ingredientAdderButton){
  ingredientAdderButton.addEventListener("click", (evt) => {
    evt.preventDefault();
    if (idIncrementer < 12){
      idIncrementer ++;
      addedIngredientsSection.insertAdjacentHTML("beforeend", 
      `<p>
          Ingredient${idIncrementer}: <input type="text"  name="ingredient${idIncrementer}" id="ingredient${idIncrementer}" placeholder="ingredient" required/>
          Measure:  <input type="text"  name="measure${idIncrementer}" id="measure${idIncrementer}" placeholder="measure" required/>
      </p>`
      )
    } else{
      ingredientAdderButton.disabled = true;
      alert("12 ingredients have been added.")
    } 
  })
}

if (ingredientRemoverButton){
  ingredientRemoverButton.addEventListener("click", (evt) => {
    evt.preventDefault();
    if (addedIngredientsSection.childNodes.length > 2){
      addedIngredientsSection.lastChild.remove();
      idIncrementer --;
    } else{
      alert("No ingredients to remove");
    }
  })
}
