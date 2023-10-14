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

first_letters = 'abcdefghijklmn'

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
            recipe = meal_dictionary["strInstructions"].replace("\r\n", " ")
            meal_image_url = meal_dictionary["strMealThumb"]
            meal_video_url = meal_dictionary["strYoutube"].replace("watch?v=", "embed/")
            
            meal_object = crud.create_meal(meal_name.title(), 
                                category.title(), 
                                area.title(),
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
                    ingredient_tuple  = (meal_object.meal_id, meal_dictionary[key].lower(), measurement,)
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
        'Irvin'
    ]

good_comments = ["Love this one. Made it a couple of times this week 💯", 
        "Where has this been all my life 🙏!!",
        "Super happy my friend recommended this app!",
        "Just starting to get into cooking again. Great first start 👨🏾‍🍳",
        "So many dishes to pick from, I almost couldn\'t choose", 
        "This app is a life saver. Hopefully they add more meals soon", 
        "This app saves me so much money 💰",  
        "So much food so little time 🤤🤤🤤",
        "This app is a keeper. Kid's enjoyed this one 👧🏻.",
        "10/10. This app is a keeper ✅!",
        "This is my love language ❤️", 
        "No way this app should be free! Too much value!",
        "Taste is okay, but I can't help but think it's not coming out right. I'll keeping giving this one a try!"
    ]

average_comments = [
    "This tasted okay. I do not think I added enough salt🧂.",
    "I was way too heavy with the salt. Almost choked to death!",
    "Not usually something I go for, but it ended up working out.",
    "Solid. Nothing to write home about. It got the job done.",
    "Mehhh",
    "Anyone got the mobile version??",
    "Not bad, not good. Average at best.",
    "I've worn thos one out. Time to move on to something 🆕",
    "Following instructions is hard."
]

bad_comments = [
    "This wasn't my favorite",
    "I wouldn't eat this again 🤮",
    "I am going to stick with eating out 🍔",
    "After eating this, I think it is safe to say that I am looking into other apps.",
    "Same dish tasted better on a different app 🤷🏾‍♂️.",
    "This one was just crazy. Who would eat this?!",
    "Man, this was bad.",
    "b-a-s-i-c"
]

#Container to split number of users in half
users_1_through_8 = []
users_9_through_16 =[]


#Create 16 users
for i in range (1, 17):
    fname = f'Test{i}'
    lname = choice(last_names)
    email = f'{fname}@gmail.com'.lower()
    password = 'test'
    user = crud.create_user(fname, lname, email, password)
    model.db.session.add(user)
    model.db.session.commit()

    for user in crud.get_all_users():
        if user.user_id <= 8: 
            users_1_through_8.append(user)
        else: 
            users_9_through_16.append(user)

    

    
#Create 10 ratings, comments, likes, dislikes, favorites for each user 
# with id 1 - 8 
for i in range(1,6):
    for user in users_1_through_8:
        random_meal = choice(meal_objects)
        random_liked_meal= choice(meal_objects[:78])
        random_disliked_meal = choice(meal_objects[78:])
        score = randint(1, 6)
        if score >=5:
            comment = choice(good_comments)
        elif score ==3 or score ==4:
            comment = choice(average_comments)
        else: 
            comment = choice(bad_comments)
        rating = crud.create_rating(user.user_id, random_meal.meal_id, score)
        comment = crud.create_comment(user.user_id , random_meal.meal_id, comment)
        like = crud.create_like(user.user_id, random_liked_meal.meal_id)
        dislike = crud.create_dislike(user.user_id, random_disliked_meal.meal_id)
        model.db.session.add(rating)
        model.db.session.add(comment)
        model.db.session.add(like)
        model.db.session.add(dislike)

#Create 10 ratings, comments, likes, dislikes, favorites for each user 
# with id 9 - 16 
for i in range(1,6):
    for user in users_9_through_16:
        random_meal = choice(meal_objects)
        random_liked_meal= choice(meal_objects[78:])
        random_disliked_meal = choice(meal_objects[:78])
        score = randint(1, 6)
        if score >=5:
            comment = choice(good_comments)
        elif score ==3 or score ==4:
            comment = choice(average_comments)
        else: 
            comment = choice(bad_comments)
        rating = crud.create_rating(user.user_id, random_meal.meal_id, score)
        comment = crud.create_comment(user.user_id , random_meal.meal_id, comment)
        like = crud.create_like(user.user_id, random_liked_meal.meal_id)
        dislike = crud.create_dislike(user.user_id, random_disliked_meal.meal_id)
        model.db.session.add(rating)
        model.db.session.add(comment)
        model.db.session.add(like)
        model.db.session.add(dislike)

model.db.session.commit()        
