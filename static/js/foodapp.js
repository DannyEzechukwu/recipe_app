// Removes all flash messages
const removeFlashButton = document.getElementById("removeflash");
const elementToRemove = document.getElementById("flash");

if (removeFlashButton) { 
  removeFlashButton.addEventListener('click', (evt) => {
      evt.preventDefault();
      elementToRemove.remove();
  })
}

// Gets last 6 comments and ratings for a user on user_details_page.html - AJAX
// Gets favorite meals for a user on user_details_page.html - AJAX
const getRecentActivityForm = document.getElementById("get-recent-activity");
const getFavoritesForm = document.getElementById("get-favorites");
const activityAndFavoritesDisplay = document.getElementById("activity-favorites-display");
const mealDetailsUserIDValue = document.getElementById("user-info-output-id");

if(getRecentActivityForm){
  getRecentActivityForm.addEventListener("submit" , (evt) => {
    evt.preventDefault();
    activityAndFavoritesDisplay.innerHTML = "";
    activityAndFavoritesDisplay.innerHTML = `
    <h1 class="header">Last 6 Ratings & Comments</h1>
      <table class="meal-rating-and-comment-or-favorite-table">
        <thead> 
          <tr>
            <th>Meal<br>Name</th>
            <th>Meal<br>Image</th>
            <th>Rating</th>
            <th>Comment</th>
            <th>Post Date</th>
          </tr>
      </thead>
      <tbody id="activity-data">
      </tbody>`;
    const activityDataSection = document.getElementById('activity-data');
    fetch(`/recent_activity/${mealDetailsUserIDValue.value}/json`)
      .then((response) => response.json())
      .then((data) => {
        data.output.forEach((output) => {
          activityDataSection.insertAdjacentHTML('beforeend', 
          `<tr>
            <td>${output.meal_name}</td>
            <td>
              <a href = "/recipe/${output.meal_name}/${output.meal_id}">
                <img src = "${output.meal_image_url}" width="100" height= "100"/>
              </a>
            </td>
            <td>${output.meal_score}</td>
            <td>${output.comment}</td>
            <td>${output.created_at}</td>
          </tr>`);
        })
      })
  })
}

if(getFavoritesForm){
  getFavoritesForm.addEventListener("submit" , (evt) => {
    evt.preventDefault();
    activityAndFavoritesDisplay.innerHTML = "";
    activityAndFavoritesDisplay.innerHTML = `
    <h1 class="header">Favorites</h1>
      <table class="meal-rating-and-comment-or-favorite-table">
        <thead> 
          <tr>
            <th>Meal<br>Name</th>
            <th>Meal<br>Image</th>
            <th>Details</th>
          </tr>
      </thead>
      <tbody id="favorite-data">
      </tbody>`;
    const favoritesDataSection = document.getElementById('favorite-data');
    fetch(`/favorites/${mealDetailsUserIDValue.value}/json`)
      .then((response) => response.json())
      .then((data) => {
        data.output.forEach((output) => {
          favoritesDataSection.insertAdjacentHTML('beforeend', 
          `<tr>
            <td>${output.meal_name}</td>
            <td>
              <a href = "/recipe/${output.meal_name}/${output.meal_id}">
                <img src = "${output.meal_image_url}" width="100" height= "100"/>
              </a>
            </td>
            <td>
              <ul style="list-style: none;">
                <li>Category : ${output.meal_category}</li>
                <li>Area : ${output.meal_area}</li>
              </ul>
            </td>
          </tr>`);
        })
      })
  })
}

// Renders meals based on inputs given on meal_picker.html - AJAX 
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

// Handles liking and disliking a meal on meal_details.html - AJAX
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

// Handles favoriting a meal on meal_details.html - AJAX
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
      addedIngredientsSection.deleteRow(addedIngredientsSection.rows.length - 1);
      idIncrementer --;
    } else{
      alert("Meal must have at least 1 ingredient");
    }
  })
}


