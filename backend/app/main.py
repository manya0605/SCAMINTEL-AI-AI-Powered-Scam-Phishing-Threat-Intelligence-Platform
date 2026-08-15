from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.app.ml.scamintel_analyzer import analyze_with_scamintel


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="SCAMINTEL AI",
    description="AI-Powered Scam, Phishing & Malicious Link Detection Platform",
    version="1.0.0"
)


# ============================================================
# REQUEST MODEL
# ============================================================

class AnalyzeRequest(BaseModel):
    message: str


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {
        "project": "SCAMINTEL AI",
        "status": "running",
        "message": "Scam detection platform is online"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "SCAMINTEL AI"
    }


# ============================================================
# MAIN ANALYSIS ENDPOINT
# ============================================================

@app.post("/analyze")
def analyze(request: AnalyzeRequest):

    if not request.message.strip():

        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    try:

        result = analyze_with_scamintel(
            request.message
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )