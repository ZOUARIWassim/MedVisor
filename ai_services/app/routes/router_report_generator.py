from app.routes.schemas import ReportGeneratorInput, ReportGeneratorOutput
from app.services.report_generator import generate_report
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def health():
    return {"message": "Report generator is running"}


@router.post("/generate_report", response_model=ReportGeneratorOutput)
def generate_full_report_endpoint(payload: ReportGeneratorInput):
    patient_data = payload.patient_data
    report_data = payload.report_data
    report_content = generate_report(patient_data, report_data)
    print(report_content.report_content)
    return ReportGeneratorOutput(report_content=report_content.report_content)
