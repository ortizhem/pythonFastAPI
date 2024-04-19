from bson import ObjectId
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

app = FastAPI()

# MongoDB connection
MONGODB_URI = "mongodb+srv://eoh:kyPpmnmSPhHgtXvH@cluster0.ybav3im.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
#client = pymongo.MongoClient(MONGODB_URI)  # Sync
client = AsyncIOMotorClient(MONGODB_URI)    # Async
db = client.get_database("testBHDB")

#customers_collection = db["customers"]
#orders_collection = db["orders"]
customers_collection = db.get_collection("customers")
orders_collection = db.get_collection("orders")

# Pydantic models for data validation
class customerItem(BaseModel):
    name: str
    email: str

class orderItem(BaseModel):
    order_id: str
    product: str
    quantity: str

@app.post("/newcustomer/")
async def create_customer(item: customerItem):
    # Save customer to MongoDB
    await customers_collection.insert_one(item.model_dump())
    return {"message": "Customer created successfully"}

@app.get("/getcustomer/{customer_id}")
async def read_customer(customer_id: str):
    # Retrieve customer from MongoDB
    item = await customers_collection.find_one({"_id": ObjectId(customer_id)})
    if item:
        print(item)
        ctr = customerItem(**item)      #pydantic use
        return ctr
    return {"message": "Customer not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)