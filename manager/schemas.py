from pydantic import BaseModel, Field
from typing import List, Optional

class Reservation(BaseModel):
    date: str = Field(..., description="The date of the reservation")
    time: str = Field(..., description="The time of the reservation")
    people: int = Field(..., description="Number of people")
    name: str = Field(..., description="Name of the person")
    reason: Optional[str] = Field(None, description="Reason for the visit")
    allergies: Optional[str] = Field(None, description="Any allergies or intolerances")

class Order(BaseModel):
    items: List[str] = Field(..., description="List of food or drink items")
    pickup_time: str = Field(..., description="Desired pickup time")
    category: str = Field(..., description="Category of the order (e.g., pizza, kitchen)")
    customer_name: str = Field(..., description="Name of the customer")

class TelephoneData(BaseModel):
    intent: str = Field(..., description="The intent of the call (reservation or order)")
    call_summary: str = Field(..., description="A short summary of the call")
