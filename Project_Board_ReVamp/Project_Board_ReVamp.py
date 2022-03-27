from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin
from werkzeug.security import generate_password_hash
from flask_security.forms import RegisterForm
from wtforms import StringField
from wtforms.validators import DataRequired
from util.validators import Unique

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)
# this is for getting the secret key
with open('../secrets.json') as f:
    data = json.load(f)

app.config['SECRET_KEY'] = data['secret_key']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Project_Board_ReVampDatabase.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_PASSWORD_HASH'] = "bcrypt"
app.config['SECURITY_PASSWORD_SALT'] = "super-secret-salt"  # !!FIX!!
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_CHANGEABLE'] = True
app.config['SECURITY_CONFIRMABLE'] = False
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_UNAUTHORIZED_VIEW'] = None

# Create database connection object
db = SQLAlchemy(app)

# Define models
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    active = db.Column(db.Boolean())
    username = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    middle_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User %r, Email %r, Name:%r %r %r>' % (
            self.username, self.email, self.first_name, self.middle_name, self.last_name)

    def __str__(self):
        return "{'id': %r, 'username': %r, 'fullname': %r}" % (self.id, self.username, self.fullname())

    def fullname(self):
        name_list = self.first_name, self.middle_name, self.last_name
        return " ".join(name for name in name_list if name.strip() != "")


class Profile(db.Model):  # !!FIX!!
    __tablename__ = "profile"
    profile_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reason = db.Column(db.String(255), nullable=False)
    training = db.Column(db.String(255))
    opportunities = db.Column(db.String(255))
    education = db.Column(db.String(255))
    study = db.Column(db.String(255))
    id = db.Column(db.Integer, db.ForeignKey(
        "users.id"), nullable=False)
    projects_id = db.Column(db.Integer, db.ForeignKey(
        "project.projects_id"))

    def __repr__(self):
        return '<Profile %r: For Project: %r  Belongs to User: %r>' % (self.profile_id, self.projects_id, self.id)


class Project(db.Model):
    __tablename__ = "project"
    projects_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_title = db.Column(db.String(255), nullable=False)
    project_type = db.Column(db.String(255), nullable=False)
    project_description = db.Column(db.String(255))
    project_duration = db.Column(db.String(255))
    project_requirements = db.Column(db.String(70), nullable=False)
    id = db.Column(db.Integer, db.ForeignKey(
        "users.id"), nullable=False)

    def __repr__(self):
        return '<Proj: %r From User: %r Title: %r>' % (self.projects_id, self.id, self.project_title)


class ExtendedRegisterForm(RegisterForm):
    username = StringField('User Name', validators=[DataRequired(), Unique(User, User.username, message='There is '
                                                                                                        'already an '
                                                                                                        'account with '
                                                                                                        'that '
                                                                                                        'username.')])
    first_name = StringField('First Name', validators=[DataRequired()])
    middle_name = StringField('Last Name')
    last_name = StringField('Last Name')


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore,
                    register_form=ExtendedRegisterForm)


# Create a user to test with
@app.before_first_request
def create_user():
    db.create_all()
    db.session.commit()
    # Create the 3 roles and an admin account
    try:
        user_datastore.create_role(name='studentUser', description='Student who joins projects.')
        user_datastore.create_role(name='partnersUser', description='Partners who creates projects.')
        admin = user_datastore.create_user(email='admin@gmail.com', password=generate_password_hash('password'),
                                           username="admin", first_name="Rahul", middle_name="Kurian",
                                           last_name="Jacob")
        role = user_datastore.create_role(name='adminUser', description='Admins who approves projects.')
        user_datastore.add_role_to_user(admin, role)
        db.session.commit()
        print(f"Fresh DB created with new admin: {admin}.")
    except:
        db.session.rollback()
        print("Previous instance of DB in-use.")


if __name__ == "__main__":
    create_user()
