// Removes flash message when a user logs in or is unable to log in
const removeFlashButton = document.getElementById("removeflash");
const elementToRemove = document.getElementById("flash");

removeFlashButton.addEventListener('click', (evt) => {
    evt.preventDefault();
    elementToRemove.remove();
})

 
  