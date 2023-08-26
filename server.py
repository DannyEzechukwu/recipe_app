from flask import Flask, render_template, request, flash, session, redirect, jsonify

from model import connect_to_db, db

import crud

from jinja2 import StrictUndefined

app = Flask(__name__)

#Secret Key to enable session
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

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

# Route containing form to input email and password
# to access application
#Data from this route is sent to /confirm_user POST route
@app.route("/login")
def login(): 

    return render_template("login.html")


#Route that allows user to input data for meals they would like returned
@app.route("/meal_picker")
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
        return redirect("/meal_picker")
    else: 
        flash("Login Unsuccessful. Try again.")
        return redirect("/login")
    


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



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)