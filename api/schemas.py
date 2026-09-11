from pydantic import BaseModel, Field
from typing import Literal

class HouseFeatures(BaseModel):
    area: float = Field(..., gt=0)
    bedrooms: int = Field(..., ge=1, le=10)
    bathrooms: int = Field(..., ge=1, le=10)
    stories: int = Field(..., ge=1, le=5)
    parking: int = Field(..., ge=0, le=5)
    mainroad: Literal["yes", "no"]
    guestroom: Literal["yes", "no"]
    basement: Literal["yes", "no"]
    hotwaterheating: Literal["yes", "no"]
    airconditioning: Literal["yes", "no"]
    prefarea: Literal["yes", "no"]
    furnishingstatus: Literal["furnished", "semi-furnished", "unfurnished"]

class PredictResponse(BaseModel):
    predicted_price: float
