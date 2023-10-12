// Removes all flash messages
const removeFlashButton = document.getElementById("removeflash");
const elementToRemove = document.getElementById("flash");

if (removeFlashButton) { 
  removeFlashButton.addEventListener('click', (evt) => {
      evt.preventDefault();
      elementToRemove.remove();
  })
}
// ---------------------------------------------------------------------------

// Gets favorite meals for a user to render in a table on user_details_page.html - JINJA LOOP
const getFavoritesForm = document.getElementById("get-favorites");
const activityAndFavoritesDisplay = document.getElementById("activity-favorites-display");
const favoritesHeader = document.getElementById("favorites-header");
const favoritesTable =  document.getElementById("favorites-table");

if (getFavoritesForm){
  getFavoritesForm.addEventListener("submit", (evt) =>{
    evt.preventDefault()
    activityAndFavoritesDisplay.innerHTML = "";
    let combinedHTML = "";
    favoritesHeader.style.display = 'block';
    favoritesTable.style.display = 'table';
    const elementsArray = [favoritesHeader, favoritesTable];
    elementsArray.forEach(element => {
      combinedHTML + element.outerHTML; // Use outerHTML to include the element's opening and closing tags
    })
    activityAndFavoritesDisplay.innerHTML = combinedHTML;
})
}
// ----------------------------------------------------------------------------

// Gets last 6 comments and ratings for a user on user_details_page.html - AJAX
const getRecentActivityForm = document.getElementById("get-recent-activity");
const mealDetailsUserIDValue = document.getElementById("user-info-output-id");

if(getRecentActivityForm){
  getRecentActivityForm.addEventListener("submit" , (evt) => {
    evt.preventDefault();
    favoritesHeader.style.display = 'none';
    favoritesTable.style.display = 'none';
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
        </tbody>
      </table>`
      ;
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
// ---------------------------------------------------------------------

// Modal functionality for areas and categories in favorites table

const modalTitle = document.getElementById("modal-title");
const modalBodyList = document.getElementById("modal-body-list");
const openModalButtons = document.querySelectorAll('[data-modal-target]');
const closeModalButtons = document.querySelectorAll('[data-modal-closer]');
const overlay = document.getElementById('overlay');

openModalButtons.forEach(button  => {
  button.addEventListener("click", (evt) => {
    evt.preventDefault();
    modalTitle.innerText = "";
    modalBodyList.innerHTML = "";
    modal.classList.add("active");
    overlay.classList.add("active");
    modalTitle.innerText = `Other ${button.value} Meals`;

    const classSearchString = "category-modal-outputer";
    const categoryQueryString = `?category=${button.value}`
    const areaQueryString = `?area=${button.value}`

    if(button.className == classSearchString){
      fetch(`/category_output/json${categoryQueryString}`)
        .then(response => response.json())
        .then(data => {
          data.category_modal_meals.forEach(( meal) => {
            modalBodyList.insertAdjacentHTML("beforeend",
            `<li><a href="/recipe/${meal.meal_name}/${meal.meal_id}">${meal.meal_name}</a></li>`
            );
          })
        })
    }else{
      fetch(`/area_output/json${areaQueryString}`)
        .then(response => response.json())
        .then(data => {
          data.area_modal_meals.forEach((meal) => {
            modalBodyList.insertAdjacentHTML("beforeend",
            `<li><a href="/recipe/${meal.meal_name}/${meal.meal_id}">${meal.meal_name}</a></li>`
            );
          })
        })
    }
  })
})


closeModalButtons.forEach(button =>{
  button.addEventListener("click", (evt) =>{
    evt.preventDefault();
    modalTitle.innerText = "";
    modalBodyList.innerHTML = "";
    modal.classList.remove("active");
    overlay.classList.remove("active");
  })
})

// --------------------------------------------------------------------
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
        bonAppétitSection = document.querySelector("#Bon-Appétit");
        mealsDiv.innerHTML = "";
        bonAppétitSection.innerHTML = "Bon Appétit!";
        data.meals.forEach((meal) => {
          const mealDiv = document.createElement("div");
          mealDiv.classList.add("meal-item");
          mealDiv.innerHTML = `
            <h4>${meal.name}</h4>
            <p>Category: ${meal.category}</p>
            <p>Area: ${meal.area}</p>
            <img src="${meal.image}" alt="${meal.name}" class="mini-meal" />
            <p><em>Contains ${meal.ingredient}</em></p>
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
// -----------------------------------------------------------------------------

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
// --------------------------------------------------------------------------

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
// -----------------------------------------------------------------------------

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





document.getElementById("back_button").addEventListener("click", function() {
  // Use the browser's history to navigate back
  history.back();
})