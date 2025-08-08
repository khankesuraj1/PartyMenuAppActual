from fastapi import FastAPI, APIRouter, HTTPException, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Data Models
class Dish(BaseModel):
    id: int
    name: str
    description: str
    image: Optional[str] = None
    mealType: str  # STARTER, MAIN_COURSE, DESSERT, SIDES
    type: str  # VEG, NON_VEG
    categoryId: int
    dishType: str
    category: Dict[str, Any]

class Ingredient(BaseModel):
    name: str
    quantity: str
    unit: str

class DishWithIngredients(BaseModel):
    dish: Dish
    ingredients: List[Ingredient]

class Selection(BaseModel):
    dish_id: int
    quantity: int = 1

class SelectionSummary(BaseModel):
    selections: List[Selection]
    total_count: int
    category_counts: Dict[str, int]

# Mock Data
MOCK_DISHES = [
    # STARTER dishes
    {
        "id": 101, "name": "Samosa", "description": "Crispy fried pastry with spiced potato filling",
        "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400", 
        "mealType": "STARTER", "type": "VEG", "categoryId": 2, "dishType": "SNACK",
        "category": {"id": 2, "name": "Indian Snacks", "image": "", "isRecommendedForMealSuggestion": True}
    },
    {
        "id": 102, "name": "Chicken Wings", "description": "Spicy grilled chicken wings with herbs",
        "image": "https://images.unsplash.com/photo-1567620832903-9fc6debc209f?w=400", 
        "mealType": "STARTER", "type": "NON_VEG", "categoryId": 3, "dishType": "GRILLED",
        "category": {"id": 3, "name": "Grilled Items", "image": "", "isRecommendedForMealSuggestion": True}
    },
    {
        "id": 103, "name": "Paneer Tikka", "description": "Marinated cottage cheese grilled to perfection",
        "image": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=400", 
        "mealType": "STARTER", "type": "VEG", "categoryId": 2, "dishType": "GRILLED",
        "category": {"id": 2, "name": "Indian Snacks", "image": "", "isRecommendedForMealSuggestion": True}
    },
    {
        "id": 104, "name": "Fish Fry", "description": "Crispy fried fish with coastal spices",
        "image": "https://images.unsplash.com/photo-1544943910-4c1dc44aab44?w=400", 
        "mealType": "STARTER", "type": "NON_VEG", "categoryId": 4, "dishType": "FRIED",
        "category": {"id": 4, "name": "Seafood", "image": "", "isRecommendedForMealSuggestion": True}
    },
    {
        "id": 105, "name": "Spring Rolls", "description": "Crispy vegetable spring rolls with sweet chili sauce",
        "image": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=400", 
        "mealType": "STARTER", "type": "VEG", "categoryId": 5, "dishType": "FRIED",
        "category": {"id": 5, "name": "Chinese", "image": "", "isRecommendedForMealSuggestion": True}
    },

    # MAIN_COURSE dishes  
    {
        "id": 201, "name": "Butter Chicken", "description": "Creamy tomato-based chicken curry",
        "image": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=400", 
        "mealType": "MAIN_COURSE", "type": "NON_VEG", "categoryId": 1, "dishType": "CURRY",
        "category": {"id": 1, "name": "North Indian", "image": "", "isRecommendedForMealSuggestion": True}
    },
    {
        "id": 202, "name": "Kadhai Paneer", "description": "Paneer cubes in spicy onion gravy with capsicum",
        "image": "https://images.unsplash.com/photo-1631452180539-96aca7d48617?w=400", 
        "mealType": "MAIN_COURSE", "type": "VEG", "categoryId": 1, "dishType": "CURRY",
        "category": {"id": 1, "name": "North Indian", "image": "", "isRecommendedForMealSuggestion": True}
    },
    {
        "id": 203, "name": "Biryani", "description": "Aromatic basmati rice with spiced meat/vegetables",
        "image": "https://images.unsplash.com/photo-1563379091339-03246963d96c?w=400", 
        "mealType": "MAIN_COURSE", "type": "NON_VEG", "categoryId": 6, "dishType": "RICE",
        "category": {"id": 6, "name": "Biryani", "image": "", "isRecommendedForMealSuggestion": True}
    },
    {
        "id": 204, "name": "Dal Tadka", "description": "Yellow lentils tempered with aromatic spices",
        "image": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400", 
        "mealType": "MAIN_COURSE", "type": "VEG", "categoryId": 1, "dishType": "DAL",
        "category": {"id": 1, "name": "North Indian", "image": "", "isRecommendedForMealSuggestion": True}
    },
    {
        "id": 205, "name": "Fish Curry", "description": "Traditional coastal fish curry with coconut",
        "image": "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=400", 
        "mealType": "MAIN_COURSE", "type": "NON_VEG", "categoryId": 4, "dishType": "CURRY",
        "category": {"id": 4, "name": "Seafood", "image": "", "isRecommendedForMealSuggestion": True}
    },

    # DESSERT dishes
    {
        "id": 301, "name": "Gulab Jamun", "description": "Sweet milk dumplings in sugar syrup",
        "image": "https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=400", 
        "mealType": "DESSERT", "type": "VEG", "categoryId": 7, "dishType": "SWEET",
        "category": {"id": 7, "name": "Indian Sweets", "image": "", "isRecommendedForMealSuggestion": True}
    },
    {
        "id": 302, "name": "Chocolate Cake", "description": "Rich chocolate sponge cake with chocolate frosting",
        "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400", 
        "mealType": "DESSERT", "type": "VEG", "categoryId": 8, "dishType": "CAKE",
        "category": {"id": 8, "name": "Cakes", "image": "", "isRecommendedForMealSuggestion": True}
    },
    {
        "id": 303, "name": "Kulfi", "description": "Traditional Indian ice cream with cardamom",
        "image": "https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=400", 
        "mealType": "DESSERT", "type": "VEG", "categoryId": 7, "dishType": "FROZEN",
        "category": {"id": 7, "name": "Indian Sweets", "image": "", "isRecommendedForMealSuggestion": True}
    },
    {
        "id": 304, "name": "Tiramisu", "description": "Italian coffee-flavored dessert",
        "image": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=400", 
        "mealType": "DESSERT", "type": "VEG", "categoryId": 9, "dishType": "LAYERED",
        "category": {"id": 9, "name": "Continental", "image": "", "isRecommendedForMealSuggestion": True}
    },

    # SIDES dishes
    {
        "id": 401, "name": "Naan", "description": "Soft Indian bread baked in tandoor",
        "image": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400", 
        "mealType": "SIDES", "type": "VEG", "categoryId": 10, "dishType": "BREAD",
        "category": {"id": 10, "name": "Breads", "image": "", "isRecommendedForMealSuggestion": True}
    },
    {
        "id": 402, "name": "Jeera Rice", "description": "Basmati rice flavored with cumin seeds",
        "image": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400", 
        "mealType": "SIDES", "type": "VEG", "categoryId": 11, "dishType": "RICE",
        "category": {"id": 11, "name": "Rice", "image": "", "isRecommendedForMealSuggestion": True}
    },
    {
        "id": 403, "name": "Raita", "description": "Yogurt-based side dish with vegetables",
        "image": "https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=400", 
        "mealType": "SIDES", "type": "VEG", "categoryId": 12, "dishType": "YOGURT",
        "category": {"id": 12, "name": "Accompaniments", "image": "", "isRecommendedForMealSuggestion": True}
    },
    {
        "id": 404, "name": "Papad", "description": "Crispy thin wafers made from lentil flour",
        "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400", 
        "mealType": "SIDES", "type": "VEG", "categoryId": 12, "dishType": "CRISPY",
        "category": {"id": 12, "name": "Accompaniments", "image": "", "isRecommendedForMealSuggestion": True}
    }
]

MOCK_INGREDIENTS = {
    101: [{"name": "Potato", "quantity": "2", "unit": "medium"}, {"name": "Onion", "quantity": "1", "unit": "small"}, {"name": "Spices", "quantity": "1", "unit": "tsp"}],
    102: [{"name": "Chicken Wings", "quantity": "500", "unit": "grams"}, {"name": "Herbs", "quantity": "2", "unit": "tbsp"}, {"name": "Spices", "quantity": "1", "unit": "tsp"}],
    103: [{"name": "Paneer", "quantity": "250", "unit": "grams"}, {"name": "Yogurt", "quantity": "2", "unit": "tbsp"}, {"name": "Spices", "quantity": "1", "unit": "tsp"}],
    201: [{"name": "Chicken", "quantity": "500", "unit": "grams"}, {"name": "Tomatoes", "quantity": "3", "unit": "medium"}, {"name": "Cream", "quantity": "100", "unit": "ml"}],
    202: [{"name": "Paneer", "quantity": "250", "unit": "grams"}, {"name": "Capsicum", "quantity": "1", "unit": "large"}, {"name": "Onion", "quantity": "2", "unit": "medium"}],
    301: [{"name": "Milk Powder", "quantity": "1", "unit": "cup"}, {"name": "Sugar", "quantity": "1", "unit": "cup"}, {"name": "Cardamom", "quantity": "4", "unit": "pods"}],
    401: [{"name": "All Purpose Flour", "quantity": "2", "unit": "cups"}, {"name": "Yogurt", "quantity": "2", "unit": "tbsp"}, {"name": "Baking Powder", "quantity": "1", "unit": "tsp"}]
}

# In-memory selections storage (in production, this would be in database)
user_selections: Dict[str, List[Selection]] = {}

# API Routes
@api_router.get("/")
async def root():
    return {"message": "Party Menu Selection API"}

@api_router.get("/dishes", response_model=List[Dish])
async def get_dishes(
    meal_type: Optional[str] = Query(None, description="Filter by meal type"),
    dish_type: Optional[str] = Query(None, description="Filter by veg/non-veg"),
    search: Optional[str] = Query(None, description="Search by dish name")
):
    dishes = MOCK_DISHES.copy()
    
    # Filter by meal type
    if meal_type:
        dishes = [d for d in dishes if d["mealType"].upper() == meal_type.upper()]
    
    # Filter by veg/non-veg
    if dish_type:
        dishes = [d for d in dishes if d["type"].upper() == dish_type.upper()]
    
    # Search by name
    if search:
        search_lower = search.lower()
        dishes = [d for d in dishes if search_lower in d["name"].lower()]
    
    return [Dish(**dish) for dish in dishes]

@api_router.get("/dishes/{dish_id}/ingredients", response_model=DishWithIngredients)
async def get_dish_ingredients(dish_id: int):
    # Find dish
    dish_data = next((d for d in MOCK_DISHES if d["id"] == dish_id), None)
    if not dish_data:
        raise HTTPException(status_code=404, detail="Dish not found")
    
    # Get ingredients
    ingredients_data = MOCK_INGREDIENTS.get(dish_id, [])
    
    return DishWithIngredients(
        dish=Dish(**dish_data),
        ingredients=[Ingredient(**ing) for ing in ingredients_data]
    )

@api_router.get("/meal-types")
async def get_meal_types():
    return {
        "meal_types": ["STARTER", "MAIN_COURSE", "DESSERT", "SIDES"],
        "display_names": {
            "STARTER": "Starter",
            "MAIN_COURSE": "Main Course", 
            "DESSERT": "Dessert",
            "SIDES": "Sides"
        }
    }

@api_router.post("/selections/{user_id}")
async def add_selection(user_id: str, selection: Selection):
    if user_id not in user_selections:
        user_selections[user_id] = []
    
    # Check if dish already selected
    existing = next((s for s in user_selections[user_id] if s.dish_id == selection.dish_id), None)
    if existing:
        existing.quantity += selection.quantity
    else:
        user_selections[user_id].append(selection)
    
    return {"message": "Selection added", "selections": user_selections[user_id]}

@api_router.delete("/selections/{user_id}/{dish_id}")
async def remove_selection(user_id: str, dish_id: int):
    if user_id in user_selections:
        user_selections[user_id] = [s for s in user_selections[user_id] if s.dish_id != dish_id]
    return {"message": "Selection removed", "selections": user_selections.get(user_id, [])}

@api_router.get("/selections/{user_id}", response_model=SelectionSummary)
async def get_selections(user_id: str):
    selections = user_selections.get(user_id, [])
    
    # Calculate category counts
    category_counts = {"STARTER": 0, "MAIN_COURSE": 0, "DESSERT": 0, "SIDES": 0}
    total_count = 0
    
    for selection in selections:
        dish = next((d for d in MOCK_DISHES if d["id"] == selection.dish_id), None)
        if dish:
            category_counts[dish["mealType"]] += selection.quantity
            total_count += selection.quantity
    
    return SelectionSummary(
        selections=selections,
        total_count=total_count,
        category_counts=category_counts
    )

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()