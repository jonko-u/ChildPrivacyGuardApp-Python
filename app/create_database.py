# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///happydb.db'  # Change the URI to match your database setup
# db = SQLAlchemy(app)
# ## Table DB scheme
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)

#     def get_id(self):
#         return str(self.id)

# with app.app_context():
#     db.create_all()

# if __name__ == '__main__':
#     app.run()