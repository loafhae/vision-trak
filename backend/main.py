from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector
from passlib.context import CryptContext

app = FastAPI()

# 1. ALLOW CONNECTIONS (CORS)
# This allows your React Web and Flutter Mobile to talk to this Python script
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. SECURITY CONFIG
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 3. DATABASE CONNECTION
def get_db():
    return mysql.connector.connect(
        host="localhost", user="root", password="", database="barangay_db"
    )

# --- MODELS (Data Structure) ---
class LoginModel(BaseModel):
    username: str
    password: str

class UserCreateModel(BaseModel):
    username: str
    password: str
    role: str
    # Add resident fields here if needed for FR1

class AnnouncementModel(BaseModel):
    title: str
    content: str

# --- API ENDPOINTS ---

# FR3: Login
@app.post("/login")
def login(user: LoginModel):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    # Check User
    cursor.execute("SELECT * FROM tbl_Users WHERE username=%s", (user.username,))
    db_user = cursor.fetchone()
    conn.close()

    if not db_user or not pwd_context.verify(user.password, db_user['password']):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    return {"status": "success", "role": db_user['role'], "user_id": db_user['user_id']}

# FR1: Add User (Admin Only)
@app.post("/users")
def create_user(user: UserCreateModel):
    conn = get_db()
    cursor = conn.cursor()
    hashed_pw = pwd_context.hash(user.password)
    
    try:
        cursor.execute("INSERT INTO tbl_Users (username, password, role) VALUES (%s, %s, %s)", 
                       (user.username, hashed_pw, user.role))
        conn.commit()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=400, detail=str(e))
    
    conn.close()
    return {"message": "User Created"}

# FR4: Get Announcements (For Mobile & Web)
@app.get("/announcements")
def get_announcements():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tbl_Announcement ORDER BY date_posted DESC")
    data = cursor.fetchall()
    conn.close()
    return data