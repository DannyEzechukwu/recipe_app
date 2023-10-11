"""CRUD operations."""

from model import db, connect_to_db,  User, Meal, Rating, Comment, Ingredient, Like, Dislike, Favorite


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
    return User.query.filter((User.email == email)).first()

#Delete a user by their email
def delete_user_by_email(email):
    user = User.query.filter((User.email == email)).first()
    print(f"User {user.user_id} deleted")
    db.session.delete(user)
    db.session.commit()
    
#-----------------------------------------------------------------------------------
#Meal crud functions

#Create meal object
def create_meal(meal_name, category, area, recipe, meal_api_id = None, meal_image_url = None,  meal_video_url = None):
    meal = Meal(meal_name = meal_name,
                category = category,
                area = area,
                recipe = recipe,
                meal_api_id = meal_api_id,
                meal_image_url = meal_image_url, 
                meal_video_url = meal_video_url)
    
    return meal

#Get all meal categories with no dupes
def get_all_categories(): 
    
    category_set = set()
    for meal in Meal.query.all(): 
        category_set.add(meal.category)
    
    return category_set

#Get all meal areas with no dupes
def get_all_areas(): 
    
    area_set = set()
    for meal in Meal.query.all(): 
        area_set.add(meal.area)
    
    return area_set

#Get all meal objects in database
def get_all_meals(): 
    return Meal.query.all()

#Get a meal object by its id
def get_meal_by_id(meal_id): 
   return Meal.query.get(meal_id)

#Get meal objects by category
def get_meal_by_category(category): 
    return Meal.query.filter(Meal.category == category.title()).all()

#Get meal objects by area
def get_meal_by_area(area):
    return Meal.query.filter(Meal.area == area.title()).all()

#Get a meal object by its name
def get_meal_by_name_and_id(meal_name, meal_id): 
   return Meal.query.filter((Meal.meal_name == meal_name) & (Meal.meal_id == meal_id)).first()

#Format meal recipe
def format_recipe(meal_recipe): 
    recipe_list = meal_recipe.split(". ")
    # standard_case_recipe_list = [line[0].upper() + line[1:] for line in recipe_list]
    print(recipe_list)

    standard_case_recipe_list = []
    for line in recipe_list: 
        new_line = line[0].upper() + line[1:]
        standard_case_recipe_list.append(new_line)
    
    print(standard_case_recipe_list)

    final_recipe_list = []

    for line in standard_case_recipe_list: 
        if "." in line: 
            line = line[:-1]
        final_recipe_list.append(line)
    
    print(final_recipe_list)
    
    return final_recipe_list

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
                #Add each meal to the meal_objects set
                meal_objects.add(Meal.query.get(meal_getter.ingredient_meal_id))
    
    #Turn meal_objects into an indexable list
    return list(meal_objects)

#Get meal objects by ingredients OR category OR area
def get_meal_by_ingredient_or_category_or_area(*ingredients, category, area):
    """ Obtain a list of melas if ingreient(s) or category
    or area are true""" 
    #Create a container to hold all meal objects returned when meal_id
    #is used to filter

    #Loop through ingredients in *ingredienst tuple
    for ingredient in ingredients:
        #Meal_objects is variable for meals returned from get_meal_by_ingredients function
        #Expetced result is a list of meal_objects
        meal_objects = get_meal_by_ingredients(ingredient)

        meal_objects.extend(Meal.query.filter((Meal.category == category) | (Meal.area == area)).all())
    
        return list(set(meal_objects))
    
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

#Get ratings by user_id and meal_id 
def get_ratings_by_user_id_and_meal_id(rating_user_id, rating_meal_id): 
    return Rating.query.filter((Rating.rating_user_id == rating_user_id) & (Rating.rating_meal_id == rating_meal_id)).all()

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
    return Comment.query.filter(Comment.comment_user_id == comment_user_id).all()

#Get comments by meal_id
def get_comments_by_meal_id(comment_meal_id): 
    return Comment.query.filter(Comment.comment_meal_id == comment_meal_id).all()

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
    return Ingredient.query.get(ingredient_id)

#Get ingredient by ingredient_name
def get_ingredient_by_name(ingredient_name):
    return Ingredient.query.filter(Ingredient.ingredient_name == ingredient_name).first()
    

def get_ingredients_by_meal_id(ingredient_meal_id): 
    return Ingredient.query.filter(Ingredient.ingredient_meal_id  == ingredient_meal_id).all()

#-----------------------------------------------------------------------------------
#Like Crud Functions

#Create Like object
def create_like(like_user_id, like_meal_id):
    like = Like(like_user_id = like_user_id,
                like_meal_id = like_meal_id)
    
    return like

#Get all like objects
def get_all_likes(): 
    return Like.query.all()

#Get like by like_id
def get_like_by_id(like_id): 
    return Like.query.get(like_id)

#Get likes by user_id
def get_likes_by_user_id(user_id): 
    return Like.query.filter(Like.like_user_id == user_id).all()

#Get likes by meal_id
def get_likes_by_meal_id(meal_id): 
   meal = Meal.query.get(meal_id)
   return meal.likes

#Get likes by meal_id and user_id
def get_like_by_user_id_and_meal_id(user_id , meal_id):
    return Like.query.filter((Like.like_user_id == user_id) & (Like.like_meal_id == meal_id)).first()
    

#-----------------------------------------------------------------------------------
#Dislike Crud Functions

#Create Dislike object
def create_dislike(dislike_user_id, dislike_meal_id):
    dislike = Dislike(dislike_user_id = dislike_user_id,
                dislike_meal_id = dislike_meal_id)
    
    return dislike

#Get all Dislike objects
def get_all_dislikes(): 
    return Dislike.query.all()

#Get dislike by dislike_id
def get_dislike_by_id(dislike_id): 
    return Dislike.query.get(dislike_id)

#Get dislike by user_id
def get_dislikes_by_user_id(user_id): 
    return Dislike.query.filter(Dislike.dislike_user_id == user_id).all()

#Get dislike by meal_id
def get_dislikes_by_meal_id(meal_id): 
    meal = Meal.query.get(meal_id)
    return meal.dislikes

#Get dislike by meal_id and user_id
def get_dislike_by_user_id_and_meal_id(user_id , meal_id):
    return Dislike.query.filter((Dislike.dislike_user_id == user_id) & (Dislike.dislike_meal_id == meal_id)).first()

#-----------------------------------------------------------------------------------
#Favorite Crud Functions

#Create Favorite object
def create_favorite(favorite_user_id, favorite_meal_id):
    favorite = Favorite(favorite_user_id = favorite_user_id,
                favorite_meal_id = favorite_meal_id)
    
    return favorite

#Get all favorite objects
def get_all_favorites(): 
    return Favorite.query.all()

#Get favorite by favorite_id
def get_favorite_by_id(favorite_id): 
    return Favorite.query.get(favorite_id)

#Get favorites by user_id
def get_favorites_by_user_id(user_id): 
    return Favorite.query.filter(Favorite.favorite_user_id == user_id).all()

#Get favorites by meal_id
def get_favorites_by_meal_id(meal_id): 
    meal = Meal.query.get(meal_id)
    return meal.favorites

#Get favorite by meal_id and user_id
def get_favorite_by_user_id_and_meal_id(user_id , meal_id):
    return Favorite.query.filter((Favorite.favorite_user_id == user_id) & (Favorite.favorite_meal_id == meal_id)).first()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)

