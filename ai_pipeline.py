import json 
from openai import AzureOpenAI
from models import InsuranceReport, InTakeForm
from config import settings


client = AzureOpenAI(
    azure_endpoint=settings.azure_openai_endpoint,
    azure_deployment=settings.azure_openai_deployemt_name,
    azure_api_version=settings.azure_openai_api_version,
    azure_key=settings.azure_openai_key
)


SYSTEM_PROMPT = """You are an expert commercial insurance analyst with 20 years of experiance assessing business risk and recommending coverage for small to mid-sized busisness.

Tour job is to analyze a client's business intake form and produce a structured insurance assessment report.
 Bespecific, practical, and thorough. Thik like a senior broker who needs to give 
a Junior broker clear guidance on what to quote.

Always respond with a valid json only -- no prose, no markdown, no explanation outside the JSON.
 """


def build_user_prompt(form: InTakeForm) -> str:
    return f""" Analyze this busniess and produce and insurance assessment report.

BUSINESS PROFILE:
- Name: {form.business_name}
- Industry: {form.industry}
- Years in operation: {form.years_in_operation}
- Employees: {form.number_of_employees}
- Annual revenue: ${form.annual_revenue:,.0f}


OPERATIONS
- Has physical location: {"Yes" if form.has_physical_location else "No"}
- Operates vehicle fleet: {"Yes" if form.operates_vehicle_fleet else "No"}
- Handles client data: {"Yes" if form.handles_client_data else "No"}    
- Provides professional advice: {"Yes" if form.provides_professional_advice else "No"}

CLAIMS HISTORY
- Prior claims count: {form.prior_claims_count if form.prior_claims_count   is not None else "N/A"}
- Prior claims description: {form.prior_claims_description if form.prior_claims_description is not None else "N/A"}         

CLIENT REQUESTED COVERAGE: 
{form.requested_coverage if form.requested_coverage is not None else "N/A"}


Respond with a JSON object matching this exact structure:
{{
  "business_name": "<string>",
  "risk_score": <integer 1-10>,
  "risk_summary": "<2-3 sentence plain-English summary of overall risk profile>",
  "coverage_recommendations": [
    {{
      "coverage_type": "<e.g. General Liability, Professional Liability, Cyber>",
      "reason": "<why this business specifically needs this>",
      "estimated_annual_premium_usd": "<e.g. $1,200 - $2,400>",
      "priority": "<essential | recommended | optional>"
    }}
  ],
  "risk_flags": [
    {{
      "flag": "<short flag title>",
      "severity": "<high | medium | low>",
      "notes": "<broker action or context>"
    }}
  ],
  "broker_notes": "<paragraph of guidance for the reviewing broker — what to watch for, what questions to ask the client, any underwriting concerns>"
}}"""


def analyze_intake(form: InTakeForm) -> InsuranceReport:
    user = build_user_prompt(form)
    response = client.chat.completions.create(
        model=settings.azure_openai_deployemt_name,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user}
        ],
        max_tokens=2048,
        temperature=0.2
    )
    raw = response.choices[0].message.content

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON response: {e}\nRaw response was: {raw}")
    return InsuranceReport(**data   )
