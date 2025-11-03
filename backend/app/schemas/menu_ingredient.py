from pydantic import BaseModel


class MenuItemIngredientBase(BaseModel):
    product_id: int
    quantity: float


class MenuItemIngredientCreate(MenuItemIngredientBase):
    pass


class MenuItemIngredientResponse(MenuItemIngredientBase):
    id: int
    menu_item_id: int
    
    class Config:
        from_attributes = True

