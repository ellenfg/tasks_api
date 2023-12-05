from typing import List, Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
# from jose import JWTError, jwt
from datetime import datetime, timedelta
# from passlib.context import CryptContext
from starlette.responses import RedirectResponse

from . import bmodels
from .models import models
from .database import SessionLocal, engine
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# @app.get("/items/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}

@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

# get all tasks
@app.get("/tasks/", response_model=List[bmodels.Task])
def show_tasks(db: Session = Depends(get_db)):
    records = db.query(models.Task).all()
    return records

# get a specific task
@app.get("/tasks/{task_id}", response_model=List[bmodels.Task])
def show_tasks(task_id: int, db: Session = Depends(get_db)):
    task_model = db.query(models.Tasks).filter(models.Tasks.task_id == task_id).first()
    return task_model

# create a new task 
# ADD IN A MESSAGE TO CONFIRM SUCCESSFUL ADDITION OF ENTRY
@app.post("/tasks/create")
def create_task(task: bmodels.CreateTask, db: Session = Depends(get_db)):

    task_model = models.Task()
    task_model.title = task.title
    task_model.description = task.description
    task_model.due_date = task.due_date

    db.add(task_model)
    db.commit()

    return task

# update a task
@app.put("/{task_id}")
def update_book(task_id: int, task: bmodels.Task, db: Session = Depends(get_db)):

    task_model = db.query(models.Tasks).filter(models.Tasks.task_id == task_id).first()

    if task_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {task_id} : Does not exist"
        )

    task_model.title = task.title
    task_model.description = task.description
    task_model.due_date = task.due_date

    db.add(task_model)
    db.commit()

    return task

# delete a task
@app.delete("/{task_id}")
def delete_book(task_id: int, db: Session = Depends(get_db)):

    task_model = db.query(models.Tasks).filter(models.Tasks.task_id == task_id).first()

    if task_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {task_id} : Does not exist"
        )

    db.query(models.Tasks).filter(models.Tasks.task_id == task_id).delete()

    db.commit()



# from typing import List

# from fastapi import Depends, FastAPI, HTTPException, status
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
# from jose import JWTError, jwt
# from datetime import datetime, timedelta
# from passlib.context import CryptContext
# from starlette.responses import RedirectResponse

# from .models import bmodels
# from .models import models
# from .database import SessionLocal, engine

# SECRET_KEY = "your-secret-key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost", "https://your-allowed-domain.com"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Dependency to get the current user from the token
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     return username


# # Dependency to get the database session
# def get_db():
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()


# # Dependency to get the current user's role
# def get_current_user_role(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.username == current_user).first()
#     return user.role


# # Function to create an access token
# def create_access_token(data: dict, expires_delta: timedelta):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + expires_delta
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# # Routes
# @app.get("/")
# def main():
#     return RedirectResponse(url="/docs/")


# @app.post("/token")
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(form_data.username, form_data.password)
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": form_data.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


# def authenticate_user(username: str, password: str):
#     user = get_user(username)
#     if user and verify_password(password, user.hashed_password):
#         return user


# def get_user(username: str, db: Session = Depends(get_db)):
#     return db.query(models.User).filter(models.User.username == username).first()


# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# # Protected route example
# @app.get("/tasks/", response_model=List[bmodels.Task])
# def show_tasks(current_user_role: str = Depends(get_current_user_role), db: Session = Depends(get_db)):
#     if current_user_role != "admin":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"
#         )
#     records = db.query(models.Task).all()
#     return records


# # Other routes with security measures...
# # ...

# # Token refresh example
# @app.post("/token/refresh")
# async def refresh_token(current_user: str = Depends(get_current_user)):
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     new_access_token = create_access_token(
#         data={"sub": current_user}, expires_delta=access_token_expires
#     )
#     return {"access_token": new_access_token, "token_type": "bearer"}
