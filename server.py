from flask import Flask, render_template, request, flash, session, redirect, jsonify

from model import connect_to_db, db

import random

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
    
    if "id" in session: 
        session.pop('id')
    
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
        session["id"] = new_user.user_id

        flash('New user added!')
        return redirect(f"/user_profile/{session['id']}")

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

#Route that allows user to input data for meals they would 
#like returned. Data goes to api/meals
@app.route("/get_a_meal")
def get_meals(): 

    categories = sorted(crud.get_all_categories())
    areas = sorted(crud.get_all_areas())

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
#Data comes from /get_a_meal
@app.route("/api/meals")
def get_meals_to_display(): 
    
    #Create a list to append dictionary of outputs that will display on
    #front end
    frontend_meals = []

    category = request.args.get("category")
    area = request.args.get("area")
    ingredient1 = request.args.get("ingredient1")
    ingredient2 = request.args.get("ingredient2")
    ingredient3 = request.args.get("ingredient3")

  
    meal_objects_list = crud.get_meal_by_ingredient_or_category_or_area(ingredient1,
                                                    ingredient2,
                                                    ingredient3,
                                                    category = category, 
                                                    area = area)
    
    for meal_object in meal_objects_list: 
        frontend_meals.append({
            "id": meal_object.meal_id,
            "name": meal_object.meal_name , 
            "image": meal_object.meal_image_url, 
            "category": meal_object.category ,
            "area":  meal_object.area
        })
    
    
    return jsonify({"meals" : random.sample(frontend_meals, 16)})


#Meal display that is shown once a meal is clicked
#Data from this route is sent to /add_rating_and comment POST route
@app.route("/recipe/<meal_name>/<int:meal_id>")
def show_meal_details(meal_name, meal_id): 

    #User in current session. Will be used to create 
    #a button to go back to profile page in meal_details_page.html
    user = crud.get_user_by_id(session["id"])

    #Obtain the meal of interest given meal_name 
    #and meal_id parameters
    meal = crud.get_meal_by_name_and_id(meal_name, meal_id)

    #Use meal relationships to get list of ingredients and comments
    meal_ingredients = meal.ingredients
    meal_comments = meal.comments
    
    meal_comments_list = []
    
    for object in meal_comments: 
        user_for_comment = crud.get_user_by_id(object.comment_user_id)
        meal_comments_list.append((user_for_comment.fname, user_for_comment.lname, object.comment, object.created_at))

    #Analyze meal_rating to get average rating
    meal_ratings = meal.ratings
    meal_rating_score_list = []

    average_score = 0 
    for rating in meal_ratings:
        meal_rating_score_list.append(rating.score)
        
        if meal_rating_score_list:
            average_score += round(sum(meal_rating_score_list) / len(meal_rating_score_list), 2)
    

    return render_template("meal_details_page.html", user = user,  
                           meal = meal, 
                           meal_ingredients = meal_ingredients,
                           average_score  = average_score,
                           meal_comments_list = meal_comments_list)
#----------------------------------------------------------------------

#ADDING DATA TO  DATABASE

#Creating a new rating and add it to the database
@app.route("/add_rating_and_comment/<meal_name>/<int:meal_id>", methods = ["POST"])
def add_rating(meal_name, meal_id):
    
    #Identify user in the session
    user_id = session["id"]
    #Rating score and comment from web page retrieved from 
    score = request.form.get("rating")
    comment = request.form.get("comment")

    #Create rating and comment Add both to database
    new_rating = crud.create_rating(user_id, meal_id, score)
    new_comment = crud.create_comment(user_id, meal_id, comment)
    db.session.add(new_rating)
    db.session.add(new_comment)
    db.session.commit()

    flash("Comment and Rating Added!")

    return redirect(f"/recipe/{meal_name}/{meal_id}")



   

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)