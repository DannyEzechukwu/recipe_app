// Removes all flash messages

const removeFlashButton = document.getElementById("removeflash");
const elementToRemove = document.getElementById("flash");

if (removeFlashButton) { 
  removeFlashButton.addEventListener('click', (evt) => {
      evt.preventDefault();
      elementToRemove.remove();
  })
}

// Renders meals based on inputs given on meal_picker.html
 
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
    
    fetch(`/get_meals/json${queryString}`)
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
            <p> Likes : ${meal.likes}</p>
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


// Handles liking and disliking a meal on meal_details.html
const userIDValue = document.getElementById("like-or-dislike-user-id");
const mealIDValue = document.getElementById("like-or-dislike-meal-id");

const likeForm = document.getElementById("like-form");
const dislikeForm = document.getElementById("dislike-form");

if(likeForm){
likeForm.addEventListener("submit", (evt) => {
  evt.preventDefault();
  fetch(`/like/${userIDValue.value}/${mealIDValue.value}/json`)
    .then((response) => response.json())
    .then((data) =>{
      let allLikes = document.getElementById("number-of-likes");
      let allDislikes = document.getElementById("number-of-dislikes");
      allLikes.innerText = data.totalLikes;
      allDislikes.innerText = data.totalDislikes;
    })
  })
}

if(dislikeForm){
  dislikeForm.addEventListener("submit", (evt) => {
    evt.preventDefault();
    fetch(`/dislike/${userIDValue.value}/${mealIDValue.value}/json`)
      .then((response) => response.json())
      .then((data) =>{
        let allLikes = document.getElementById("number-of-likes");
        let allDislikes = document.getElementById("number-of-dislikes");
        allLikes.innerText = data.totalLikes;
        allDislikes.innerText = data.totalDislikes;
      })
    })
  }



//Include or Remove ingredients for the meal being added on the add_a_meal.html

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
      ` <tr>
          <td>Ingredient${idIncrementer} <span class="required-asterisk">*</span> <input type="text"  name="in${idIncrementer}" id="ingredient${idIncrementer}" placeholder="ingredient" required/></td>
          <td>Measure <span class="required-asterisk">*</span>  <input type="text"  name="measure${idIncrementer}" id="measure${idIncrementer}" placeholder="measure" required/></td>
          <td>Ingredient Image (url)  <input type="url"  name="url${idIncrementer}" id="url${idIncrementer}" placeholder="ingredient image url"/></td>
        </tr>`
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
    if (addedIngredientsSection.rows.length > 1){
      // addedIngredientsSection.lastChild.remove();
      addedIngredientsSection.deleteRow(addedIngredientsSection.rows.length - 1);
      idIncrementer --;
    } else{
      alert("Meal must have at least 1 ingredient");
    }
  })
}
