"""Models for food recipe and ratings app"""

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

#db object to represent database
db = SQLAlchemy()

def connect_to_db(flask_app, db_uri="postgresql:///food", echo=False):
        flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
        flask_app.config["SQLALCHEMY_ECHO"] = echo
        flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        db.app = flask_app
        db.init_app(flask_app)

        print("Connected to the db!")


#User Table
class User(db.Model): 
    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                        primary_key = True,
                        autoincrement = True)
    
    fname = db.Column(db.String, 
                    index = True, 
                    nullable = False)
    
    lname = db.Column(db.String,
                    index = True,
                    nullable = False)
    
    email = db.Column(db.String,
                    index = True, 
                    nullable = False, 
                    unique = True)
    
    password = db.Column(db.String,
                    index = True, 
                    nullable = False)
    
    created_at = db.Column(db.DateTime, 
                            default = datetime.now())
    
    #User can have many comments
    comments = db.relationship("Comment", back_populates = "user")
    #User can have many ratings
    ratings = db.relationship("Rating", back_populates = "user")
    
    def __repr__(self): 
          return f'<User user_id = {self.user_id}, email = {self.email}>'
    
    

#Meal Table
class Meal(db.Model): 
    __tablename__ = "meals"

    meal_id = db.Column(db.Integer, 
                    primary_key = True,
                    autoincrement = True)
    
    meal_name = db.Column(db.String, 
                    index = True, 
                    nullable = False)
    
    category = db.Column(db.String, 
                    index = True, 
                    nullable = False)

    
    area = db.Column(db.String,
                    index = True,
                    nullable = False)
    
    recipe = db.Column(db.Text,
                    index = True, 
                    nullable = False)
    
    meal_image_url = db.Column(db.String,
                    index = True, 
                    nullable = False)
    
    meal_video_url = db.Column(db.String,
                    index = True, 
                    nullable = False)
    
    #Meal can have many comments
    comments = db.relationship("Comment", back_populates = "meal")
    #Meal can have many ratings
    ratings = db.relationship("Rating", back_populates = "meal")
    #Meal can have many ingredients
    ingredients = db.relationship("Ingredient", back_populates = "meal")
    
    
    def __repr__(self): 
        return f'<Meal meal_id = {self.meal_id}, name = {self.meal_name}, area = {self.area}>'
    
#Ratings Table
class Rating(db.Model): 
    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, 
                        primary_key = True,
                        autoincrement = True)
    
    rating_user_id = db.Column(db.Integer,
                    db.ForeignKey('users.user_id'),
                    index = True)
    
    rating_meal_id = db.Column(db.Integer,
                    db.ForeignKey('meals.meal_id'),
                    index = True)
    
    score = db.Column(db.Integer,
                    index = True, 
                    nullable = False)
    
    created_at = db.Column(db.DateTime, 
                        default = datetime.now())
    
    #Rating can belong to one user
    user = db.relationship("User", back_populates = "ratings")
    #Rating can belong to one meal
    meal = db.relationship("Meal", back_populates = "ratings")
    
    def __repr__(self): 
          return f'<Rating user_id = {self.user_id}, meal_id = {self.rating_user_id}, score = {self.score}>'
    
#Comments Table
class Comment(db.Model): 
    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, 
                    primary_key = True,
                    autoincrement = True)
    
    comment_user_id = db.Column(db.Integer,
                    db.ForeignKey('users.user_id'),
                    index = True)
    
    comment_meal_id = db.Column(db.Integer,
                    db.ForeignKey('meals.meal_id'),
                    index = True)
    
    comment = db.Column(db.Text,
                    index = True, 
                    nullable = False)
    
    #Comment can belong to one user
    user = db.relationship("User", back_populates = "comments")
    #Comment can belong to one meal
    meal = db.relationship("Meal", back_populates = "comments")
    
    created_at = db.Column(db.DateTime, 
                             default = datetime.now())

    def __repr__(self): 
        return f'<Comment comment_id = {self.comment_id}, comment_user_id={self.comment_user_id}>'
    
#Ingredients Table
class Ingredient(db.Model): 
    ingredient_id = db.Column(db.Integer, 
                        primary_key = True,
                        autoincrement = True)
    
    ingredient_meal_id = db.Column(db.Integer,
                    db.ForeignKey('meals.meal_id'),
                    index = True)
    
    ingredient_name = db.Column(db.String,
                    index = True, 
                    nullable = False)
    
    ingredient_measure = db.Column(db.Integer,
                    index = True, 
                    nullable = False)
    
    ingredient_image_url = db.Column(db.String,
                    index = True)
    
    #An ingredient can belong to one meal
    meal = db.relationship("Meal", back_populates = "ingredients")
    def __repr__(self): 
        return f'<Ingredient ingredient_id = {self.ingredient_id}, ingredient_meal_id= {self.ingredient_meal_id}, ingredient_name = {self.ingredient_name}>'

    
   


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app, echo=False)