"""Script to seed food database"""

import os
import json
from random import choice, randint

import crud
import model
import server

os.system("dropdb food")
os.system('createdb food')
model.connect_to_db(server.app)
model.db.create_all()

first_letters = 'abcdefghijklmnopqrstuvwxyz'
cook_times = ["10 min", "15 min", "20 min", "30 min", "45 min", "60 min", "90 min"]

with open('data/data.json') as f:
    meal_data = json.loads(f.read())

# Initialize list to hold data for meal table
#Wlill be used to populate database
meal_objects = []

#Initialize kist to hold data for ingredients table
ingredients = []
ingredient_objects = []

for letter in first_letters:
    if meal_data[letter]['meals']:
        for meal_dictionary in meal_data[letter]['meals']: 
            meal_api_id = int(meal_dictionary["idMeal"])
            meal_name = meal_dictionary['strMeal']
            category = meal_dictionary["strCategory"]
            area = meal_dictionary["strArea"]
            cook_time = choice(cook_times)
            recipe = meal_dictionary["strInstructions"].replace("\r\n", " ")
            meal_image_url = meal_dictionary["strMealThumb"]
            meal_video_url = meal_dictionary["strYoutube"].replace("watch?v=", "embed/")
            
            meal_object = crud.create_meal(meal_name, 
                                category, 
                                area,
                                cook_time,
                                recipe,
                                meal_api_id,
                                meal_image_url, 
                                meal_video_url)
            
            meal_objects.append(meal_object)
            model.db.session.add_all(meal_objects)
            model.db.session.commit()
             
            #Access each key in eah meal dictionary that exists in list 
            #returned from meal_data[letter]["meals"]
            for key in meal_dictionary:
                #Check if "strIngredient" exists within the key of a dictionary
                if "strIngredient" in key:
                    #Remove strIngredient prefix to get access to integer
                    measure_ingredient_number = key.removeprefix("strIngredient")
                    #Obtain the measurement that corresponds to the integer returned
                    #Return "chef's preference" if measurementis not available
                    measurement = meal_dictionary.get(f'strMeasure{measure_ingredient_number}', "Chef's Preference")
                    #Create a tuple that contains ingredient name, measurement and meal_id
                    ingredient_tuple  = (meal_object.meal_id, meal_dictionary[key].title(), measurement,)
                    ingredients.append(ingredient_tuple)

                    #Loop through each tuple in ingredients set
                    for tuple in ingredients: 
                    #Create an Ingredient object
                        ingredient_object = crud.create_ingredient(tuple[0],
                                tuple[1], 
                                tuple[2],
                                f"http://www.themealdb.com/images/ingredients/{tuple[1]}.png")

                    ingredient_objects.append(ingredient_object)
                    model.db.session.add_all(ingredient_objects)
                    model.db.session.commit()
    

last_names = ['Smith', 
              'Jones', 
              'Dodson', 
              'Albert', 
              'Cole', 
              'Fitzgerald', 
              'Robinson',
              'Vincent', 
              'Parsons', 
              'Long', 
              'Murray',
              'Nolen',
              'Turner', 
              'Owens', 
              'Edwards',
              'Farris',
              'Gregory',
              'Williams',
              'Harrison',
              'Knight',
              'Bowens',
              'Irvin']

comments = [
            "This tasted okay. I do not think I added enough salt. 🧂",
            "Love this one. Made it a couple of times this week. 💯",
            "This wasn't my favorite.", 
            "Where has this been all my life.",
            "I was way to heavy with the salt. Almost choked to death!",
            "Super happy my friend recommended this app!",
            "I probably wouldn't eat this again.🤮",
            "Just starting to get into cooking again. Great first start. 👨🏾‍🍳",
            "So many dishes to pick from. I almost couldn\'t choose.", 
            "This app is a life saver. Hopefully the creator adds more meals soon.", 
            "This app saves me so much money. 💰", 
            "I am going to stick with eating out. 🍔", 
            "So much food so little time. 🤤🤤🤤",
            "Not usually something I go for, but it ended up working out.",
            "After eating this, I think it is safe to say that I am looking into other apps.",
            "Solid. Nothing to write home about. It got the job done. ",
            "This site is a keeper. Kid's enjoyed this one. 👧🏻",
            "10/10. This app is a keeper! ✅",
            "Mehhh.",
            "Same dish tasted better on a different app. 🤷🏾‍♂️",
            "Anyone got the mobile version??",
            "This is my love language. ❤️", 
            "No way this app should be free! Too much value!"]

#Container to hold user objects to add to database 
user_objects = []

#Create 15 users
for i in range (1, 16):
    fname = f'Test{i}'
    lname = choice(last_names)
    email = f'{fname}@gmail.com'.lower()
    password = 'test'
    user = crud.create_user(fname, lname, email, password)
    model.db.session.add(user)
    model.db.session.commit()
    

    
    #Create user ratings comments
    for _ in range(1,15):
        random_meal = choice(meal_objects)
        score = randint(1, 6)
        comment = choice(comments)
        rating = crud.create_rating(user.user_id, random_meal.meal_id, score)
        comment = crud.create_comment(user.user_id, random_meal.meal_id, comment)
        model.db.session.add(rating)
        model.db.session.add(comment)
        



 
model.db.session.commit()        
