from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.services.auth_services import get_current_user

router = APIRouter(prefix="/cart", tags=["Shopping Cart"])


def get_or_create_cart(user_id: int, db: Session):
    cart = db.query(models.Cart).filter(models.Cart.user_id == user_id).first()
    if not cart:
        cart = models.Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


def build_cart_response(cart: models.Cart, db: Session):
    rows = (
        db.query(models.CartItem, models.Product)
        .join(models.Product, models.CartItem.product_id == models.Product.id)
        .filter(models.CartItem.cart_id == cart.id)
        .all()
    )

    items = [
        {
            "id": item.id,
            "product_id": product.id,
            "unit_price": product.price,
            "quantity": item.quantity,
        }
        for item, product in rows
    ]
    return {"id": cart.id, "user_id": cart.user_id, "items": items}


@router.get(
    "/", response_model=schemas.cart.CartResponse, status_code=status.HTTP_200_OK
)
def view_cart(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    cart = get_or_create_cart(current_user.id, db)
    return build_cart_response(cart, db)


@router.post(
    "/items", response_model=schemas.CartResponse, status_code=status.HTTP_201_CREATED
)
def add_to_cart(
    item_in: schemas.cart.CartItemAdd,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    row = (
        db.query(models.Product, models.Inventory)
        .join(models.Inventory, models.Product.id == models.Inventory.product_id)
        .filter(models.Product.id == item_in.product_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")
    product, inventory = row
    available = inventory.stock_quantity - inventory.reserved_quantity

    cart = get_or_create_cart(current_user.id, db)

    existing_item = (
        db.query(models.CartItem)
        .filter(
            models.CartItem.cart_id == cart.id,
            models.CartItem.product_id == item_in.product_id,
        )
        .first()
    )
    new_quantity = item_in.quantity + (existing_item.quantity if existing_item else 0)

    if new_quantity > available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only {available} units available in the stock",
        )
    if existing_item:
        existing_item.quantity = new_quantity
    else:
        new_item = models.CartItem(
            cart_id=cart.id,
            product_id=item_in.product_id,
            quantity=new_quantity,
        )
        db.add(new_item)

    db.commit()
    return build_cart_response(cart, db)


@router.patch("/items/{product_id}", response_model=schemas.cartResponse)
def update_cart_item(
    product_id: int,
    item_in: schemas.cart.CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    cart = get_or_create_cart(current_user.id, db)
    cart_item = (
        db.query(models.CartItem)
        .filter(
            models.CartItem.cart_id == cart.id, models.CartItem.product_id == product_id
        )
        .first()
    )
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in the cart")

    if item_in.quantity == 0:
        db.delete(cart_item)
    else:
        Inventory = (
            db.query(models.Inventory)
            .filter(models.Inventory.product_id == product_id)
            .first()
        )

        available = Inventory.stock_quantity - Inventory.reserved_quantity

        existing_item = (
            db.query(models.CartItem)
            .filter(
                models.CartItem.cart_id == cart.id,
                models.CartItem.product_id == item_in.product_id,
            )
            .first()
        )
        new_quantity = item_in.quantity + (
            existing_item.quantity if existing_item else 0
        )
        if item_in.quantity > new_quantity:
            raise HTTPException(
                status_code=400, detail=f"Only {available} units available in the stock"
            )
        cart_item.quantity = item_in.quantity
    db.commit()
    return build_cart_response(cart, db)
