from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import UserOut, UserProfileUpdate, AddressCreate, AddressUpdate
from models.user import User, Address  # Assuming Address is defined in models
from database import get_db
from api.auth import get_current_user

router = APIRouter()

@router.get("/profile", response_model=UserOut)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/profile", response_model=UserOut)
def update_profile(user_update: UserProfileUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/address-book")
def get_address_book(current_user: User = Depends(get_current_user)):
    # Assuming user has an address_book attribute
    return current_user.addresses

@router.post("/address-book")
def add_address(address: AddressCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_address = Address(**address.dict(), user_id=current_user.id)
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address

@router.put("/address-book/{address_id}")
def update_address(address_id: int, address_update: AddressUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    address = db.query(Address).filter(Address.id == address_id, Address.user_id == current_user.id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    for key, value in address_update.dict(exclude_unset=True).items():
        setattr(address, key, value)
    db.commit()
    db.refresh(address)
    return address

@router.delete("/address-book/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    address = db.query(Address).filter(Address.id == address_id, Address.user_id == current_user.id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(address)
    db.commit()
    return {"msg": "Address deleted successfully"}
