from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum 

class Industry(str, Enum):
    construction = "construction"
    retail = "retail"
    hospitality = "hospitality"
    technology = "technology"
    retail = "retail"
    manufacturing = "manufacturing"
    services = "services"
    hospitality = "hospitality"
    other = "other"


class InTakeForm(BaseModel):
    business_name: str = Field(..., description="The name of the business")
    industry: Industry = Field(..., description="The industry the business operates in")
    years_in_operation: int = Field(ge=0, description="The number of years the business has been in operation")
    number_of_employees: int = Field(ge=1, description="The number of employees in the business")
    annual_revenue: float = Field(gt=0, description="The annual revenue of the business")

    #optional fields
    has_physical_location: Optional[bool] = Field(None, description="Whether the business has a physical location")
    operates_vehicle_fleet: Optional[bool] = Field(None, description="Whether the business operates a vehicle fleet")
    handles_client_data: Optional[bool] = Field(None, description="Whether the business handles client data")
    provides_professional_advice: Optional[bool] = Field(None, description="Whether the business provides professional advice")

    #Claims history 
    prior_claims_count: Optional[int] = Field(None, description="The number of prior claims the business has had")
    prior_claims_description: Optional[str] = Field(None, description="A brief description of the prior claims, if any") or Field(None, description="A brief description of the prior claims, if any")

    #coverage 
    requested_coverage: Optional[str] = Field(None, description="The type of coverage the business is requesting")


class CoverageRecommendation(BaseModel):
    recommended_coverage: str = Field(..., description="The recommended type of coverage for the business")
    rationale: str = Field(..., description="The rationale behind the coverage recommendation")
    estimated_anual_premium_usd: str = Field(..., description="The estimated annual premium in USD for the recommended coverage")
    priority:str = Field(..., description="The priority level of the recommendation (e.g., high, medium, low)")


class RiskFlag(BaseModel):
    flag: str = Field(..., description="The type of risk flag (e.g., high risk industry, prior claims history)")
    severity: str = Field(..., description="the sevrity of the flag (e.g., high, medium, low)")
    notes: Optional[str] = Field(None, description="Additional notes or context about the risk flag")


class InsuranceReport(BaseModel):
    business_name: str = Field(..., description="The name of the business")
    industry: Industry = Field(..., description="The industry the business operates in")
    coverage_recommendation: CoverageRecommendation = Field(..., description="The recommended coverage for the business")
    risk_score: int = Field(..., ge=0, le=100, description="The overall risk score for the business on a scale of 0 to 100")
    risk_flags: Optional[list[RiskFlag]] = Field(None, description="A list of identified risk flags for the business")
    broker_notes: Optional[str] = Field(None, description="Additional notes from the insurance broker regarding the business or the recommendation")
    disclaimer: str = (
        "This report is AI-generated and must be reviewed by a licensed insurance "
        "broker before being presented to the client. It does not constitute a "
        "binding quote or insurance advice."
    )