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
const theMealForm = document.querySelector("#get-meal-options-form");

if (theMealForm){
  theMealForm.addEventListener('submit', (evt) => {
    evt.preventDefault();
    const ingredientOne  = document.querySelector("#ingredient1").value;
    const ingredientTwo = document.querySelector("#ingredient2").value;
    const ingredientThree = document.querySelector("#ingredient3").value;
    const ingredientFour = document.querySelector("#ingredient4").value;
    const queryString = `ingredient1=${ingredientOne}&ingredient2=${ingredientTwo}&ingredient3=${ingredientThree}&ingredient4=${ingredientFour}`;
    
    fetch(`/get_meals/json?${queryString}`)
      .then((response) => response.json())
      .then((data) => {
        const mealsDiv = document.getElementById("returned-meals");
        mealsDiv.innerHTML = "";
        data.meals.forEach((meal) => {
          const mealDiv = document.createElement("div");
          mealDiv.classList.add("meal-item");
          mealDiv.innerHTML = `
            <h4>${meal.name}</h4>
            <p>Category: ${meal.category}</p>
            <p>Area: ${meal.area}</p>
            <img src="${meal.image}" alt="${meal.name}" class="mini-meal" />
            <p><em>Contains ${meal.ingredient}</em></p>
            <p>⏱️${meal.cook_time} </p>
            <p>👍 ${meal.likes}</p>
            <p>
            <a href="/recipe/${meal.name}/${meal.id}">
              <button class = "button"> Explore Meal </button> 
            </a>
            </p>
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

const voteYes = document.getElementById("vote-yes");
const voteNo = document.getElementById("vote-no");

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
      voteYes.style.backgroundColor = "blue";
      voteNo.style.backgroundColor = "green";
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
        voteNo.style.backgroundColor = "red";
        voteYes.style.backgroundColor = "green";
    })
  })
}

// Handles favoriting a meal on meal_details.html
const favoriteForm = document.getElementById("favorite-form");
const favorite = document.getElementById("favorite");

if(favoriteForm){
favoriteForm.addEventListener("submit", (evt) => {
  evt.preventDefault();
  fetch(`/favorite/${userIDValue.value}/${mealIDValue.value}/json`)
    .then((response) => response.json())
    .then((data) =>{
      if (data.favorite == "yes") {
        favorite.style.backgroundColor = "blue";
      } else{
        favorite.style.backgroundColor = "green";
      } 
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
