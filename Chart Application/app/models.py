from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# -------------------- User Model --------------------
# Represents a user in the system (admin or regular user)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)                  # Unique user ID
    username = Column(String, unique=True, index=True)                 # Username must be unique
    password = Column(String)                                          # Hashed password
    role = Column(String)                                              # 'admin' or 'user'

    # Optional: If you want to access messages sent by user (can add later)
    # messages = relationship("Message", back_populates="user")

# -------------------- Room Model --------------------
# Represents a chat room where users can exchange messages
class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)                 # Unique room ID
    name = Column(String, unique=True, index=True)                    # Room name (must be unique)

    # One-to-many relationship: One room → many messages
    messages = relationship("Message", back_populates="room")

# -------------------- Message Model --------------------
# Represents a message sent by a user in a specific room
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)                # Unique message ID
    content = Column(String)                                          # Message text content
    timestamp = Column(DateTime, default=datetime.utcnow)            # Timestamp of when message was sent

    user_id = Column(Integer, ForeignKey("users.id"))                 # Reference to sender (User)
    room_id = Column(Integer, ForeignKey("rooms.id"))                 # Reference to room where message was sent

    # Link back to Room model (so you can access message.room)
    room = relationship("Room", back_populates="messages")

    # Optional: If you want reverse relationship from User (can add if needed)
    # user = relationship("User", back_populates="messages")
