import requests
import json

#Alphabet string to serve argument in API to retrieve all meals in the database
first_letters = 'abcdefghijklmnopqrstuvwxyz'

#API URL to get all meal details by first letter
url = "http://www.themealdb.com/api/json/v2/9973533/search.php?f="

#Initialize an empty dictionary to hold all meals in the database
meal_by_letter_dictionary = {}

#Loop through each letter in first_letters string
for letter in first_letters:
    #Add a key, value pair to the dictionary that follows the pattern - {letter : apiresult} 
    meal_by_letter_dictionary[letter] = requests.get(f'{url}{letter}').json()

#Create variable to hold the string to the file_path where the data will be placed
file_path= 'data/data.json'

#Open the file_path and load meal_by_letter_dictionary
with open(file_path, "w") as f:
    #Loop through each letter in first_letters string
    #print(meal_by_letter_dictionary['v']['meals'])
    for letter in first_letters:
        if meal_by_letter_dictionary[letter]['meals']:
    #Loop through each dictionary in the list that is 
    #returned from meal_by_letter_dictionary[letter][meals]
    #if no list is returned, the default value is an empty list
            for meal_dict in meal_by_letter_dictionary[letter]['meals']:
            #Condition for if meal_dict is does evaluate to []
            #Establish a range from 1 - 20. Each meal has a max of 20 ingredients and 20 measures
                for i in range(1, 21): 
                #Conditions for if an ingrient key and measure key evaluate to an empty string or None
                    if meal_dict[f'strIngredient{i}'] == "" or meal_dict[f'strIngredient{i}'] == None:
                        #if condition is true, remove key value pair from meal_object
                        del meal_dict[f'strIngredient{i}']
                    
                    if meal_dict[f'strMeasure{i}'] == "" or meal_dict[f'strMeasure{i}'] == " " or meal_dict[f'strMeasure{i}'] == None:
                        #if condition is true, remove key value pair from meal_object
                        del meal_dict[f'strMeasure{i}']
                
    json.dump(meal_by_letter_dictionary, f)
    

