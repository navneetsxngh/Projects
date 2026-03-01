from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated

from config.city_tier import tier_1_cities, tier_2_cities

# Pydantic Model to validate incoming Data
class UserInput(BaseModel):

    age: Annotated[int, Field(..., gt=0, lt=100, description="Age of the User")]
    weight: Annotated[float, Field(..., gt=0, lt=150, description="Weight of the User")]
    height: Annotated[float, Field(..., gt=0, lt=2.5, description="Height of the User")]
    income_lpa: Annotated[float, Field(..., gt=0, description="Annual Salary of the User (in LPA)")]
    smoker: Annotated[bool, Field(..., description="Is User a Smoker")]
    city: Annotated[str, Field(..., description="The City that the user belong to")]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job'], Field(..., description="Occupation of the User")]


    @field_validator('city')
    @classmethod
    def normalise_city(cls, v: str) -> str:
        v = v.strip().title()
        return v

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height**2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "High"
        elif self.smoker and self.bmi > 27:
            return "Medium"
        else:
            return "Low"
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "Young"
        elif self.age < 45:
            return "Adult"
        elif self.age < 60:
            return "Middle_Aged"
        else:
            return "Senior"
            
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3