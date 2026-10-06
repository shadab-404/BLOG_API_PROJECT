from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import engine, get_db
import auth
import models
import schemas

models.base.metadata.create_all(bind=engine)

app = FastAPI()


# HOME ROUTE
@app.get("/")
def home():
    return {"message": "Welcome to my blog API"}


# REGISTER USER
@app.post(
    "/auth/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(
        username=user.username,
        password_hash=auth.hash_password(user.password),
    )
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already registered",
        ) from None
    db.refresh(new_user)
    return new_user


# LOGIN AND ISSUE JWT
@app.post("/auth/login", response_model=schemas.TokenResponse)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    account = db.query(models.User).filter(
        models.User.username == user.username
    ).first()
    if account is None or not auth.verify_password(
        user.password, account.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "access_token": auth.create_access_token(account.username),
        "token_type": "bearer",
    }


# CREATE BLOG
@app.post(
    "/blog",
    response_model=schemas.BlogResponse,
    dependencies=[Depends(auth.get_current_user)],
)
def create_blog(
    blog: schemas.BlogCreate,
    db: Session = Depends(get_db),
):
    new_blog = models.Blog(title=blog.title, content=blog.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# READ ALL BLOGS
@app.get("/blog", response_model=list[schemas.BlogResponse])
def get_all_blogs(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()


# GET BLOG BY ID
@app.get("/blog/{id}", response_model=schemas.BlogResponse)
def get_blog_by_id(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with the id {id} is not available")
    return blog


# UPDATE BLOG BY ID
@app.put(
    "/blog/{id}",
    response_model=schemas.BlogResponse,
    dependencies=[Depends(auth.get_current_user)],
)
def update_blog(
    id: int,
    blog: schemas.BlogCreate,
    db: Session = Depends(get_db),
):
    existing_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not existing_blog:
        raise HTTPException(status_code=404, detail=f"Blog with the id {id} is not available")

    existing_blog.title = blog.title
    existing_blog.content = blog.content
    db.commit()
    db.refresh(existing_blog)
    return existing_blog
    
# DELETE BLOG BY ID
@app.delete(
    "/blog/{id}",
    dependencies=[Depends(auth.get_current_user)],
)
@app.delete(
    "/blogs/{id}",
    include_in_schema=False,
    dependencies=[Depends(auth.get_current_user)],
)
def delete_blog(
    id: int,
    db: Session = Depends(get_db),
):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=404,
            detail=f"Blog with the id {id} is not available",
        )

    db.delete(blog)
    db.commit()
    return {"message": "blog deleted"}

 
    
