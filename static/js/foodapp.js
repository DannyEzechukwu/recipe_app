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


// Generate random meal id between 55,000 and 60,000 on
// add_a_meal page
const generateMealIdButton = document.getElementById("get-meal-id");
const mealId = document.getElementById("meal-id");

if (generateMealIdButton){
  generateMealIdButton.addEventListener("click", (evt) => {
    evt.preventDefault();
    mealId.value = randomId = Math.floor(Math.random() * (60000 - 55000) + 55000);
  })
}


//Include or Remove ingredients for the meal being added on the add_a_meal page
const ingredientAdderButton = document.getElementById("ingredient-adder");
const ingredientRemoverButton = document.getElementById('ingredient-remover');
const addedIngredientsSection = document.getElementById("ingredients");
// unique identifier for id and name for ingredient elements
let idIncrementer = 0;
// incrementer to keep number of ingredients added to no more than 12 
let ingredientsAdded = 0; 

if (ingredientAdderButton){
  ingredientAdderButton.addEventListener("click", (evt) => {
    evt.preventDefault();
    if (ingredientsAdded < 12){
      ingredientsAdded ++;
      idIncrementer ++;
      addedIngredientsSection.insertAdjacentHTML("beforeend", 
      `<p>
          Ingredient${idIncrementer}: <input type="text"  name="ingredient${idIncrementer}" id="ingredient${idIncrementer}" placeholder="ingredient" />
          Measure:  <input type="text"  name="measure${idIncrementer}" id="measure${idIncrementer}" placeholder="measure" />
          Ingredient Image (url):  <input type="text" name="image${idIncrementer}" id="image${idIncrementer}" placeholder="ingredient image url" />
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
    } else{
      alert("No ingredients to remove");
    }
  })
}

// Add a Meal
// JS handle submit event on the form to prevent default behavior
// JS build the object for the new meal that you are going to submit
/*  
{ category: "beef", area: "America", ingredients: [
  {name: "food1", quantity: "5 cups"},
  {name: "food2", quantity: "3 Tbsp"}
] }

fetch("/create_meal", {}) // set type to POST, and add above object as the body


BACKEND
request.form.get() ^ object as a complete object
additional processing so that it becomes a meal object with a list of ingredients
add that object to the database all at once
*/
