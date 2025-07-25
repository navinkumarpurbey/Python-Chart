from pydantic import BaseModel
from typing import Optional

# -------------------- User Schemas --------------------

# Schema used when a user signs up (required: username, password, and role)
class UserCreate(BaseModel):
    username: str          # Unique name for the user
    password: str          # Plaintext password (will be hashed)
    role: str              # Either 'admin' or 'user'

# Schema used when a user logs in
class UserLogin(BaseModel):
    username: str          # Username for login
    password: str          # Password for login

# -------------------- Room Schema --------------------

# Schema for creating a new chat room
class RoomCreate(BaseModel):
    name: str                           # Name of the room
    description: Optional[str] = None  # Optional room description

# -------------------- Message Schema --------------------

# Schema for posting a new message in a chat room
class MessageCreate(BaseModel):
    room_id: int           # ID of the room where the message is sent
    content: str           # The actual text message content
