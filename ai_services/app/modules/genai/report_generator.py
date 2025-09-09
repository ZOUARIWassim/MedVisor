import logging

from app.models.app import MedicalReport, MedicalReportData
from app.utils.gemini_content_generator import generate_content
from google.genai import types
from jinja2 import Environment, PackageLoader

logger = logging.getLogger(__name__)

env = Environment(loader=PackageLoader("app.modules.genai", "templates"))


def generate_report_metadata(
    patient_data: dict, model: str = "gemini-2.5-flash"
) -> MedicalReportData:
    template = env.get_template("report_metadata_gen.jinja")
    contents = [template.render(patient_data=patient_data)]
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=MedicalReportData,
        thinking_config=types.ThinkingConfig(thinking_budget="512"),
    )
    response = generate_content(model, contents, config)

    if isinstance(response, MedicalReportData):
        return response
    else:
        logger.error("Response is not a MedicalReportData")
        raise ValueError("Response is not a MedicalReportData")


def generate_full_report(
    report_data: MedicalReportData, patient_data: dict, model: str = "gemini-2.5-flash"
) -> MedicalReport:
    template = env.get_template("full_report_gen.jinja")
    contents = [template.render(report_data=report_data, patient_data=patient_data)]

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=MedicalReport,
        thinking_config=types.ThinkingConfig(thinking_budget="512"),
    )
    response = generate_content(model, contents, config)
    if isinstance(response, MedicalReport):
        return response
    else:
        logger.error("Response is not a MedicalReport")
        raise ValueError("Response is not a MedicalReport")
    return response
