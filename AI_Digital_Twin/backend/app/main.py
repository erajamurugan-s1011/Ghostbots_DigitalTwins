from app.database import engine
from app.models.user import User
from app.models.chat import Chat

from app.dependencies import get_current_user

User.metadata.create_all(bind=engine)

from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services.ai_service import generate_reply
from app.services.document_service import extract_pdf_text
from app.services.embedding_service import store_text
from app.services.file_service import extract_text
from app.database import get_db
from app.models.user import User
from app.schemas.user import (
    UserRegister,
    UserLogin
)
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token
)




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message":"Backend Connected Successfully"}


@app.post("/chat")
async def chat(
    data: ChatRequest,
    user=Depends(get_current_user),
    db: Session=Depends(get_db)
):

    reply=generate_reply(
        data.message
    )

    new_chat=Chat(

        user_email=user,
        question=data.message,
        answer=reply
    )

    db.add(new_chat)

    db.commit()

    return{
        "reply":reply
    }


@app.get("/history")
async def history(
    user=Depends(get_current_user),
    db:Session=Depends(get_db)
):

    chats=db.query(Chat).filter(
        Chat.user_email==user
    ).all()

    results=[]

    for item in chats:

        results.append({

            "question":
            item.question,

            "answer":
            item.answer
        })

    return results


@app.post("/upload")
async def upload(
    file: UploadFile,
    user=Depends(get_current_user)
):

    try:

        text = extract_text(file)

        if not text:

            return {
                "message":"Unsupported or empty file"
            }

        store_text(text)

        return {
            "message":"Document stored successfully"
        }

    except Exception as e:

        print("UPLOAD ERROR:", e)

        return {
            "message": str(e)
        }

@app.post("/register")
async def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:

        return {
            "message":
            "Email already exists"
        }

    new_user = User(

        username=user.username,
        email=user.email,
        password=hash_password(
            user.password
        )
    )

    db.add(new_user)
    db.commit()

    return {
        "message":
        "User created successfully"
    }


@app.post("/login")
async def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:

        return {
            "message":
            "User not found"
        }

    if not verify_password(
        user.password,
        db_user.password
    ):

        return {
            "message":
            "Wrong password"
        }

    token = create_access_token(
        {
            "sub":
            db_user.email
        }
    )

    return {
        "token": token
    }