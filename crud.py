"""CRUD operations."""

from model import db, connect_to_db,  User, Meal, Rating, Comment, Ingredient


#User crud functions
#Create user object
def create_user(fname, lname, email, password): 
    user = User(fname = fname, lname = lname, email = email, password = password)
    return user

#Get all user objects from database
def get_all_users(): 
    return User.query.all()

#Get a user object by its user_id
def get_user_by_id(user_id): 
    return User.query.get(user_id)

#Get a user object by their email
def get_user_by_email(email): 
    return User.query.filter(User.email == email).first()

#-----------------------------------------------------------------------------------
#Meal crud functions

#Create meal object
def create_meal(meal_name, category, area, recipe, meal_image_url = None,  meal_video_url = None):
    meal = Meal(meal_name = meal_name,
                category = category,
                area = area, 
                recipe = recipe, 
                meal_image_url = meal_image_url, 
                meal_video_url = meal_video_url)
    
    return meal

#Get all meal objects in database
def get_all_meals(): 
    return Meal.query.all()

#Get a meal object by its id
def get_meal_by_id(meal_id): 
   return Meal.query.get(meal_id)

#Get meal objects by ingredients only
def get_meal_by_ingredients(*ingredients):
    """Obtain a list of meals from an input of ingredient(s)"""

    #Generate a set container to hold all meals objects returned
    #and avoid duplicates
    #If tomato returns salad, we do not want to get salad from onions as well
    meal_objects = set()
    #Loop through all of the ingredients entered in *ingredients tuple
    for ingredient in ingredients: 
        #Create a list of ingredient objects for each ingredient in *ingredients tuple
        #by running a filter query to match the name of each ingredient
        ingredient_objects_list = Ingredient.query.filter(Ingredient.ingredient_name == ingredient).all()

        #Condition for if ingredient entered returns a list
        if ingredient_objects_list:
            #Loop through each object in the list returned
            for meal_getter in ingredient_objects_list:
                #Get a meal by running a get query to get meal_id in the meals table
                #that exists as meal_id in the ingredients table
                #Append each meal to the container
                meal_objects.add(Meal.query.get(meal_getter.ingredient_meal_id))
    
    #Turn meal_objects into an indexable list
    return list(meal_objects)

#Get meal objects by ingredients AND category AND area
def get_meal_by_ingredient_and_category_and_area(*ingredients, category = None, area = None):
    """Obtain a list of meals if ingredients, 
    category, and area are true
    """
    #Create a container to hold all meal objects returned when meal_id
    #is used to filter
    meal_results = []

    #Loop through ingredients in *ingredienst tuple
    for ingredient in ingredients:
        #meal_objects is variable for meals returned from get_meal_by_ingredients function
        #Expetced result is a list of unique meal_objects
        meal_objects = get_meal_by_ingredients(ingredient)
    
    #Condition for if meal objects is an empty list 
    if meal_objects == []:
        #return filter result for category and area
        return Meal.query.filter((Meal.category == category) & (Meal.area == area)).all()
    
    #Condition for if category is not provided
    elif category == None:
        #Loop through meal_objects list
        for meal_object in meal_objects: 
            #Append filter result for area and meal_id to meal_results
            return meal_results.append(Meal.query.filter((Meal.area == area) & (Meal.meal_id == meal_object.meal_id)))

    #Condition for if area is not provided
    elif area == None: 
        #Loop through meal_objects list
        for meal_object in meal_objects: 
            #Append filter result for category and meal_id to meal_results
            return meal_results.append(Meal.query.filter((Meal.category == category) & (Meal.meal_id == meal_object.meal_id)))

    #Condition for if meal_objects is an empty list and area is not provided
    elif meal_objects == [] and area == None: 
        #Return filter result for category
        return Meal.query.filter(Meal.category == category).all()
    
    #Condition for if meal_objects is an empty list and category is not provided
    elif meal_objects == [] and category == None: 
        #Return filter result for area 
        return Meal.query.filter(Meal.area == area).all()
    
    #Condition for if category and area not provided
    elif category == None and area == None: 
        #Loop through meal_objects list
        for meal_object in meal_objects:
            #Append filter result for meal_id to meal_results
            return meal_results.append(Meal.query.get(meal_object.meal_id))

#Get meal objects by ingredients OR category OR area
def get_meal_by_ingredient_or_category_or_area(*ingredients, category, area):
    """ Obtain a list of melas if ingreient(s) or category
    or area are true""" 
    #Create a container to hold all meal objects returned when meal_id
    #is used to filter
    meal_results = []

    #Loop through ingredients in *ingredienst tuple
    for ingredient in ingredients:
        #Meal_objects is variable for meals returned from get_meal_by_ingredients function
        #Expetced result is a list of meal_objects
        meal_objects = get_meal_by_ingredients(ingredient)
    
    #Condition for if meal objects is an empty list
    if meal_objects ==[]:
        #return filter result for category or area
        return Meal.query.filter((Meal.category == category) | (Meal.area == area)).all()
    
    #Condition for if category is not provided
    elif category == None:
        #Loop through meal_objects list
        for meal_object in meal_objects: 
            #Append filter result for area or meal_id to meal_results
            return Meal.query.filter((Meal.area == area) | (Meal.meal_id == meal_object.meal_id)).all()

    #Condition for if area is not provided
    elif area == None: 
        #Loop through meal_objects list
        for meal_object in meal_objects: 
            #Append filter result for category or meal_id to meal_results
            return Meal.query.filter((Meal.category == category) | (Meal.meal_id == meal_object.meal_id)).all()

    #Condition for if meal_objects is an empty list and area is not provided
    elif meal_objects == [] and area == None: 
        #Return filter result for category
        return Meal.query.filter(Meal.category == category).all()
    
    #Condition for if meal_objects is an empty list and category is not provided
    elif meal_objects == [] and category == None: 
        #Return filter result for area 
        return Meal.query.filter(Meal.area == area).all()
    
    #Condition for if category and area not provided
    elif category == None and area == None: 
        #Loop through meal_objects list
        for meal_object in meal_objects:
            #Append filter result for meal_id to meal_results
            return meal_results(Meal.query.get(meal_object.meal_id))


#------------------------------------------------------------------------------------------
#Rating crud functions

#Create rating object
def create_rating(rating_user_id, rating_meal_id, score): 
    rating = Rating(rating_user_id = rating_user_id, 
                rating_meal_id = rating_meal_id, 
                score = score)
    
    return rating

#Get all ratings in database
def get_all_ratings(): 
    return Rating.query.all()

#Get rating by rating_id
def get_rating_by_id(rating_id): 
    return Rating.query.get(rating_id)

#Get ratings by user_id
def get_ratings_by_user_id(rating_user_id): 
    return Rating.query.filter(Rating.rating_user_id == rating_user_id).all()

#Get ratings by meal_id
def get_ratings_by_meal_id(rating_meal_id): 
    return Rating.query.filter(Rating.rating_meal_id == rating_meal_id).all()

#---------------------------------------------------------------------------------
#Comment crud functions

#Create comment object
def create_comment(comment_user_id, commnent_meal_id, comment): 
    comment = Comment(comment_user_id = comment_user_id, 
                      comment_meal_id = commnent_meal_id, 
                      comment = comment)
    
    return comment

#Get all comments in database
def get_all_comments(): 
    return Comment.query.all()

#Get comment by comment_id
def get_comment_by_id(comment_id): 
    return Comment.query.get(comment_id)

#Get comments by user_id
def get_comments_by_user_id(comment_user_id): 
    return Rating.query.filter(Comment.comment_user_id == comment_user_id).all()

#Get comments by meal_id
def get_comments_by_meal_id(comment_meal_id): 
    return Rating.query.filter(Comment.comment_meal_id == comment_meal_id).all()

#-----------------------------------------------------------------------------------
#Ingredient crud functions

#Create ingredient object
def create_ingredient(ingredient_meal_id,
                    ingredient_name,
                    ingredient_measure, 
                    ingredient_image_url = None):
    
    ingredient = Ingredient(ingredient_meal_id = ingredient_meal_id, 
                ingredient_name = ingredient_name, 
                ingredient_measure= ingredient_measure, 
                ingredient_image_url = ingredient_image_url)
    
    return ingredient

#Get all ingredients
def get_all_ingredients(): 
    return Ingredient.query.all()

#Get ingredient by ingredient_id
def get_ingredient_by_id(ingredient_id): 
    return Comment.query.get(ingredient_id)

def get_ingredients_by_meal_id(ingredient_meal_id): 
    return Ingredient.query.filter(ingredient_meal_id  == ingredient_meal_id).all()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)

