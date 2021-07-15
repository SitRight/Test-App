from typing import Optional
from fastapi import FastAPI, File, UploadFile
import connection
from bson import ObjectId
from json import dumps
from schematics.models import Model
from schematics.types import StringType, EmailType
from fastapi.middleware.cors import CORSMiddleware


class User(Model):
    user_id = ObjectId()
    email = EmailType(required=True)
    name = StringType(required=True)


# An instance of class User
newuser = User()

# funtion to create and assign values to the instanse of class User created
def create_user(email, username, password):
    newuser.user_id = ObjectId()
    newuser.email = email
    newuser.name = username
    return dict(newuser)

def email_exists(email):
    user_exist = True
    if connection.db.users.find(
        {'email': email}
    ).count() == 0:
        user_exist = False
        return user_exist

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Our root endpoint
@app.get("/")
def index():
    return {"message": "Hello World"}

# Signup endpoint with the POST method
@app.post("/signup/{email}/{username}")
def signup(email, username: str):
    user_exists = False
    data = create_user(email, username)

    # Covert data to dict so it can be easily inserted to MongoDB
    dict(data)

    # Checks if an email exists from the collection of users
    if connection.db.users.find(
        {'email': data['email']}
        ).count() > 0:
        user_exists = True
        print("User Exists")
        return {"message":"User Exists"}
    # If the email doesn't exist, create the user
    elif user_exists == False:
        connection.db.users.insert_one(data)
        return {"message":"User Created","email": data['email'], "name": data['name']}

@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}