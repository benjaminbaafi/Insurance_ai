
from config import settings
from fastapi import fastAPI, HTTPException
from models import InTakeForm, InsuranceReport
from ai_pipeline import  analyze_intake


app = FastAPI(
    title="Insurance AI",
    description="An AI-powered insurance recommendation engine that analyzes business intake forms to provide coverage recommendations and risk assessments.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"status": "Insurance AI is running. Submit a POST request to /analyze with the business intake form data.",
            "product":  "Insurance AI",
            "model":"settings.azure_openai_deployemt_name",
            }

@app.post("/analyze", response_model=InsuranceReport)
def analyze(form: InTakeForm):
    try:
        report = analyze_intake(form)
        return report
    except ValueError  as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/health")
def health_check():
    return {"status":"ok", "endpoint" : settings.azure_openai_deployemt_name}


