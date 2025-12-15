from pydantic import BaseModel
from typing import List

class RFPAnalysis(BaseModel):
    business_goals: List[str]
    technical_requirements: List[str]
    non_functional_requirements: List[str]
    constraints: List[str]

class ArchitectureDesign(BaseModel):
    overview: str
    services: List[str]
    availability: str
    security: str
    diagram_steps: List[str]

class CostEstimate(BaseModel):
    monthly_cost: str
    yearly_cost: str
    assumptions: List[str]
