from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    user_id: int
    
    class Config:
        from_attributes = True

class MapSearchBase(BaseModel):
    location_name: str
    search_time: str

class MapSearchCreate(MapSearchBase):
    user_id: int

class MapSearch(MapSearchBase):
    search_id: int
    user_id: int

    class Config:
        from_attributes = True

class TravelDistanceBase(BaseModel):
    distance_km: float = Field(..., gt=0)
    destination: str

class TravelDistanceCreate(TravelDistanceBase):
    user_id: int

class TravelDistance(TravelDistanceBase):
    travel_id: int
    user_id: int

    class Config:
        from_attributes = True

class NearbyPlaceBase(BaseModel):
    place_name: str
    category: Optional[str] = None

class NearbyPlaceCreate(NearbyPlaceBase):
    user_id: int

class NearbyPlace(NearbyPlaceBase):
    place_id: int
    user_id: int

    class Config:
        from_attributes = True

class NotificationBase(BaseModel):
    notification_time: str
    esp32_pushed_time: Optional[str] = None
    app_name: str
    content: str

class NotificationCreate(NotificationBase):
    user_id: int

class Notification(NotificationBase):
    notification_id: int
    user_id: int

    class Config:
        from_attributes = True

# Base64 Response Wrapper
class B64Response(BaseModel):
    data: str  # Base64 encoded JSON
