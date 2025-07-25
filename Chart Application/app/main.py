from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict
import json
from jose import JWTError, jwt

from . import models, schemas, auth, database, deps

# Initialize FastAPI application
app = FastAPI()

# Automatically create all tables in the database on startup
models.Base.metadata.create_all(bind=database.engine)

# Enable CORS so frontend clients (like React) can connect without restriction
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- AUTHENTICATION ROUTES --------------------

# Register a new user with hashed password and assigned role
@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    hashed_pw = auth.hash_password(user.password)
    db_user = models.User(username=user.username, password=hashed_pw, role=user.role)
    db.add(db_user)
    db.commit()
    return {"msg": "User created"}

# Login route to verify user credentials and return a JWT token
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(auth.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

# Protected route only accessible to users with admin role
@app.get("/admin-only")
def protected(admin: str = Depends(deps.admin_required)):
    return {"msg": "Welcome, Admin!"}

# -------------------- CHAT ROOM & MESSAGE ROUTES --------------------

# Create a new chat room
@app.post("/rooms/")
def create_room(room: schemas.RoomCreate, db: Session = Depends(auth.get_db)):
    db_room = models.Room(name=room.name, description=room.description)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

# Post a message to a specific room; requires valid JWT
@app.post("/messages/")
def post_message(msg: schemas.MessageCreate, token: str = Depends(auth.oauth2_scheme), db: Session = Depends(auth.get_db)):
    payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
    username = payload.get("sub")
    
    # Find the user who sent the message
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Save the message to the database
    db_msg = models.Message(content=msg.content, room_id=msg.room_id, user_id=user.id)
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg

# Retrieve all messages from a room (ordered by most recent first)
@app.get("/rooms/{room_id}/messages/")
def get_room_messages(room_id: int, db: Session = Depends(auth.get_db)):
    messages = db.query(models.Message).filter(models.Message.room_id == room_id).order_by(models.Message.timestamp.desc()).all()
    return messages

# -------------------- WEBSOCKET CHAT ROUTE --------------------

# Store active WebSocket connections by room_id
active_connections: Dict[int, List[WebSocket]] = {}

# WebSocket endpoint for real-time chat in a room
@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, token: str = ""):
    try:
        # Decode and validate the JWT token sent via query parameter
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username = payload.get("sub")

        # If token is invalid or missing username, reject the connection
        if not username:
            await websocket.close()
            return
    except JWTError:
        # If decoding the token fails, reject the connection
        await websocket.close()
        return

    # Accept the WebSocket connection
    await websocket.accept()

    # Register this connection in the active connection pool for the room
    if room_id not in active_connections:
        active_connections[room_id] = []
    active_connections[room_id].append(websocket)

    try:
        while True:
            # Wait for message from client
            data = await websocket.receive_text()

            # Broadcast received message to all other clients in the same room
            for conn in active_connections[room_id]:
                if conn != websocket:
                    await conn.send_text(json.dumps({"user": username, "msg": data}))
    except WebSocketDisconnect:
        # On disconnect, remove the client from the active pool
        active_connections[room_id].remove(websocket)
