from app.models.ai_request_enum import AiRequestType
from app.service.initialize_service import medical_speciality_service
from app.service.medical_specialities_service import MedicalSpecialitiesService


# class AiRequestType(Enum):
#     Blood_Test = "Blood Test"
#     Radiology_Report = "Radiology Report"
#     ECG_Report = "ECG Report"
#     EEG_Report = "EEG Report"

class Prompts:

    def __init__(self, ai_request_type: AiRequestType):
        self.ai_request_type = ai_request_type
        self.str_prompt: str = """
        
        You are an AI medical assistant tasked with analyzing various medical reports, 
        including EEG, ECG, blood tests, and radiology reports (CT scan, MRI, U/S). 
        Please carefully read the document provided and give the following information based on the symptoms:
        
        Diagnosis: A short summary of the condition or findings based on the report.
        Treatment: Suggested treatments or next steps to address the diagnosis.
        Doctor Specialty: The medical specialist (e.g., cardiologist, neurologist, general physician) who can best handle the treatment or further evaluation.
        suggestions : e.g. Follow up after 6 months, Monitor heart rate
        
        If the document is not related to EEG, ECG, blood tests, or radiology reports (CT scan, MRI, U/S), 
        respond with the following JSON format:
        {
            "diagnosis": "Please provide a proper document",
            "treatment": "Error",
            "doctors_recommended": [],
            "suggestions": []
        }
        
        
        If the document shows no significant symptoms or findings, respond with:
        Your Response format will be in json like:
        {
            "diagnosis": "Your report looks fine. No need to worry",
            "treatment": "No treatment required",
            "doctors_recommended": [],
            "suggestions": ["No suggestions needed"]
        }
        
        If symptoms are found,
        Your Response format will be in json like:
        {
            "diagnosis": "short diagnosis here...",
            "treatment": "suggested treatment here...",
            "doctors_recommended": ["specialist type here..."],
            "suggestions" : ["Monitor heart rate", "etc"]
        }

        """

    def get_prompt(self):
        return self.str_prompt

    def get_instructions(self):
        instructions = {
            AiRequestType.Blood_Test: "Ensure your results are clear and legible.",
            AiRequestType.Radiology_Report: "Include the full report for accurate analysis.",
            AiRequestType.ECG_Report: "Attach the report in PDF format.",
            AiRequestType.EEG_Report: "Make sure to include all necessary data."
        }
        return instructions.get(self.ai_request_type, "Invalid request type.")

    def get_response_type(self):
        response_types = {
            AiRequestType.Blood_Test: "Detailed analysis of blood parameters.",
            AiRequestType.Radiology_Report: "Interpretation of radiology findings.",
            AiRequestType.ECG_Report: "ECG interpretation and recommendations.",
            AiRequestType.EEG_Report: "EEG analysis and potential diagnoses."
        }
        return response_types.get(self.ai_request_type, "Invalid request type.")

    def get_format_type(self):
        return """
        {
                "diagnosis": "",
                "treatment": "",
                "doctors_recommended": ["list of strings is any"],
                "suggestions" : ["list of strings is any"]
            }
        """

    def get_merged_prompt(self,):
        prompt = self.get_prompt()
        instructions = self.get_instructions()
        response_type = self.get_response_type()
        merged_request = f"{prompt}\n\nInstructions: {instructions}\n\nExpected Response Type: {response_type}"
        return merged_request

# todo
    async def get_specialities(self) -> str:
        data = ''
        specialities = await medical_speciality_service.get_medical_specialities_names()

        if specialities:
            for speciality in specialities:
                data += speciality['name'] + ', '
            data = data.rstrip(', ')

        return data