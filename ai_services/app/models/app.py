from datetime import date

from pydantic import BaseModel, Field


class ChiefComplaint(BaseModel):
    """
    Represents the main reason for the patient's visit.
    """

    complaint_text: str = Field(..., description="The patient's chief complaint.")
    onset_date: date | None = Field(None, description="The date the complaint started.")


class HistoryOfPresentIllness(BaseModel):
    """
    Detailed description of the current illness.
    """

    history_text: str = Field(..., description="Narrative describing the current illness.")


class Diagnosis(BaseModel):
    """
    Represents a medical diagnosis.
    """

    diagnosis_code: str = Field(..., description="Standardized diagnosis code (e.g., ICD-10).")
    diagnosis_description: str = Field(
        ..., description="Human-readable description of the diagnosis."
    )


class Medication(BaseModel):
    """
    Represents a medication.
    """

    medication_name: str = Field(..., description="Name of the medication.")
    dosage: str = Field(..., description="Dosage of the medication (e.g., 500 mg).")
    frequency: str = Field(..., description="Frequency of administration (e.g., twice daily).")


class LaboratoryResult(BaseModel):
    """
    Represents a single laboratory test result.
    """

    test_name: str = Field(..., description="Name of the lab test.")
    result_value: str = Field(..., description="The result value.")
    units: str = Field(..., description="Units of measurement (e.g., g/dL).")
    reference_range: str = Field(..., description="Normal reference range for the test.")


class MedicalReportData(BaseModel):
    """
    A comprehensive medical report object.
    """

    report_date: date = Field(..., description="Date the report was generated.")
    chief_complaint: ChiefComplaint = Field(..., description="The patient's chief complaint.")
    history_of_present_illness: HistoryOfPresentIllness = Field(
        ..., description="Detailed history of the current illness."
    )
    diagnoses: list[Diagnosis] = Field(..., description="List of diagnoses.")
    medications: list[Medication] = Field(..., description="List of prescribed medications.")
    laboratory_results: list[LaboratoryResult] = Field(..., description="List of lab test results.")
    plan_of_care: str = Field(
        ..., description="The recommended plan of care or follow-up instructions."
    )

    class Config:
        schema_extra = {
            "example": {
                "report_date": "2025-09-09",
                "chief_complaint": {
                    "complaint_text": "Chest pain and shortness of breath.",
                    "onset_date": "2025-09-05",
                },
                "history_of_present_illness": {
                    "history_text": "Patient is a 40-year-old male with a history of hypertension who presents with a 4-day history of exertional chest pain. The pain is described as a pressure-like sensation radiating to the left arm and is associated with shortness of breath."
                },
                "diagnoses": [
                    {
                        "diagnosis_code": "I25.10",
                        "diagnosis_description": "Atherosclerotic heart disease of native coronary artery without angina pectoris.",
                    }
                ],
                "medications": [
                    {"medication_name": "Aspirin", "dosage": "81 mg", "frequency": "daily"},
                    {"medication_name": "Lisinopril", "dosage": "10 mg", "frequency": "daily"},
                ],
                "laboratory_results": [
                    {
                        "test_name": "Troponin T",
                        "result_value": "0.15",
                        "units": "ng/mL",
                        "reference_range": "<0.01 ng/mL",
                    },
                    {
                        "test_name": "LDL Cholesterol",
                        "result_value": "150",
                        "units": "mg/dL",
                        "reference_range": "<100 mg/dL",
                    },
                ],
                "plan_of_care": "Admit to cardiology service. Order coronary angiogram. Start patient on beta-blocker and statin therapy. Consult with cardiothoracic surgery.",
            }
        }


class MedicalReport(BaseModel):
    report_content: str = Field(
        ..., description="The formatted medical report content as a string."
    )
