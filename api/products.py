from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from models.product import Product  # Assuming a Product model is defined
from schemas.product import ProductCreate, ProductUpdate, ProductOut
from database import get_db

router = APIRouter()

@router.get("/", response_model=list[ProductOut])
def get_products(db: Session = Depends(get_db), page: int = 1, pageSize: int = 10, **filters):
    query = db.query(Product)

    # Apply filters like category, price range, etc.
    if "category" in filters:
        query = query.filter(Product.category == filters["category"])

    # Pagination
    products = query.offset((page - 1) * pageSize).limit(pageSize).all()
    return products

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return None
