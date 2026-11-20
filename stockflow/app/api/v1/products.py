from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.services.auth_services import get_current_user

router = APIRouter(prefix="/products", tags=["Products & Categories"])


@router.post(
    "/categories",
    response_model=schemas.product.CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    cat_in: schemas.product.CategoryCreate,
    db: Session = Depends(get_db),
):
    try:
        new_cat = models.Category(
            name=cat_in.name,
            slug=cat_in.slug,
            parent_id=cat_in.parent_id,
        )
        db.add(new_cat)
        db.commit()
        db.refresh(new_cat)
        return new_cat
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category slug already exists or invalid parent_id",
        )


@router.post(
    "/",
    response_model=schemas.product.ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product_in: schemas.product.ProductCreate,
    db: Session = Depends(get_db),
):
    if product_in.category_id is not None:
        cat = (
            db.query(models.Category)
            .filter(models.Category.id == product_in.category_id)
            .first()
        )
        if not cat:
            raise HTTPException(status_code=404, detail="Category not found")
    try:
        new_product = models.Product(
            name=product_in.name,
            description=product_in.description,
            price=product_in.price,
            category_id=product_in.category_id,
        )
        db.add(new_product)
        db.flush()

        new_inventory = models.Inventory(
            product_id=new_product.id,
            stock_quantity=product_in.initial_stock,
            reserved_quantity=0,
        )
        db.add(new_inventory)
        db.commit()
        db.refresh(new_product)
        db.refresh(new_inventory)

        return {
            "product": new_product,
            "inventory": new_inventory,
        }

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Database integrity error")


@router.get("/", response_model=list[schemas.product.ProductWithInventoryResponse])
def list_products(db: Session = Depends(get_db)):
    rows = (
        db.query(models.Product, models.Inventory)
        .outerjoin(models.Inventory, models.Product.id == models.Inventory.product_id)
        .all()
    )
    return [{"product": p, "inventory": inv} for p, inv in rows]
