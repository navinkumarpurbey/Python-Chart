from fastapi import Depends, HTTPException, Header
from .auth import get_user_role

def admin_required(role: str = Depends(get_user_role)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
