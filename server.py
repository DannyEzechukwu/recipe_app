from flask import Flask, render_template, request, flash, session, redirect, jsonify

from model import connect_to_db, db

import crud

from jinja2 import StrictUndefined

app = Flask(__name__)

#Secret Key to enable session
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

#LOGIN FUNCTINALITY

# Home page where user has the option to login or 
# create an account
@app.route("/")
def welcome_page(): 
    
    return render_template('welcome_page.html')

# Route containing form to create account
# Data from this route is sent to /new_user POST route
@app.route("/create_account")
def create_account():
    
    return render_template("create_account.html")

# Create a new user using the POST route new_user
# Add this user to the data base if the email dos not exist
@app.route('/new_user', methods = ['POST'])
def register_user():
    
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")

    if crud.get_user_by_email(email): 
        flash('You cannot create an account with this email. Try again.')
        return redirect('/')
    else: 
        new_user = crud.create_user(fname, lname, email, password)
        db.session.add(new_user)
        db.session.commit()

        flash('New user added!')
        return redirect("/meal_picker")

# Route containing form to input email and password
# to access application
#Data from this route is sent to /confirm_user POST route
@app.route("/login")
def login(): 

    return render_template("login.html")

#Check if email is in db. If it is, allow the user 
# to enter application and start session.
#If it it not have them try to sign in again.
@app.route("/confirm_user", methods = ["POST"])
def confirm():
    
    email = request.form.get("email")

    current_user = crud.get_user_by_email(email)

    if current_user: 
        session["id"] = current_user.user_id
        flash("Login Successful!")
        return redirect(f"/user_profile/{current_user.user_id}")
    else: 
        flash("Login Unsuccessful. Try again.")
        return redirect("/login")
#-------------------------------------------------------------------

#USER PROFILE

#Route that displays a user's 6 most recent ratings and comments
@app.route("/user_profile/<int:user_id>")
def user_profile(user_id):
    if 'id' in session: 

        #Identify user by value of session["id"]
        user = crud.get_user_by_id(user_id)

        #Container to hold name of meals rated
        meals_scored = []
        #Container to hold rated meal image url
        rated_meal_images = []
        #Container to rating scores
        rating_scores = []
        #Container to hold comment user maid on meal
        meal_comments = []
        #Container to hold  dates and times scores were given
        rating_and_comment_created_at = []

        #List of ratings given by user in the session
        ratings = crud.get_ratings_by_user_id(user_id)
        for rating in ratings:
            rating_scores.append(rating.score)
            rating_and_comment_created_at.append(rating.created_at)

            meal = crud.get_meal_by_id(rating.rating_meal_id)
            meals_scored.append((meal.meal_name , meal.meal_id))
            rated_meal_images.append(meal.meal_image_url)
        
        comments = crud.get_comments_by_user_id(user_id)
        for comment in comments:
            meal_comments.append(comment.comment)

        #Zip lists to get elements in following format
        #(name_of_meal, score, time_created)
        meal_scores_comments_and_times = list(zip(meals_scored, 
                                    rated_meal_images, 
                                    rating_scores, 
                                    meal_comments, 
                                    rating_and_comment_created_at ))


    return render_template("user_details_page.html", 
                        user = user,
                        meal_scores_comments_and_times = meal_scores_comments_and_times)


#-------------------------------------------------------------------

#MEAL DISPLAYS

#Route that allows user to input data for meals they would like returned
@app.route("/get_a_meal")
def get_meals(): 

    categories = crud.get_all_categories()
    areas = crud.get_all_areas()

    ingredients_set = set()
    ingredients = crud.get_all_ingredients()
    for ingredient in ingredients: 
        ingredients_set.add(ingredient.ingredient_name)
    
    ingredients_list = sorted(list(ingredients_set))

    return render_template("meal_picker.html", 
                    categories = categories,
                    areas = areas,
                    ingredients = ingredients_list)


#Route to run ajax on meals page as inputs are changed
@app.route("/api/meals")
def get_meals_to_display(): 
    
    #Create a list to append dictionary of outputs that will display on
    #front end
    frontend_meals = []

    category = request.args.get("and-category")
    area = request.args.get("and-area")
    ingredient1 = request.args.get("and-ingredient1")
    ingredient2 = request.args.get("and-ingredient2")
    ingredient3 = request.args.get("and-ingredient3")

  
    meal_objects_list = crud.get_meal_by_ingredient_and_category_and_area(ingredient1,
                                                    ingredient2,
                                                    ingredient3,
                                                    category, 
                                                    area)
    

    for meal_object in meal_objects_list: 
        frontend_meals.append({
            "name": meal_object.meal_name , 
            "category": meal_object.meal_category ,
            "area":  meal_object.area, 
            "recipe" : meal_object.recipe, 
            "meal_image_url": meal_object.meal_image_url,
            "meal_video_url": meal_object.meal_video_url
            })
    
    return jsonify({"meals" : frontend_meals})

@app.route("/recipe/<meal_name>/<int:meal_id>")
def show_meal_details(meal_name, meal_id): 

    meal = crud.get_meal_by_name_and_id(meal_name, meal_id)

    meal_ingredients = meal.ingredients
    meal_comments = meal.comments

    return render_template("meal_details_page.html", meal = meal, 
                           meal_ingredients = meal_ingredients)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)