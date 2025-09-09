import logging

from app.models.app import MedicalReport
from app.modules.genai.report_generator import generate_full_report, generate_report_metadata

logger = logging.getLogger(__name__)


def generate_report(patient_data: dict, report_data: dict) -> MedicalReport:
    # Generate structured metadata from patient data
    structured_report_data = generate_report_metadata(patient_data)
    # Generate the full formatted report
    report_content = generate_full_report(structured_report_data, patient_data)
    return report_content
