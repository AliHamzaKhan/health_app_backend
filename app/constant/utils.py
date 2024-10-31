import json
import textwrap
from typing import Tuple

# from rich import Console

from app.models.data_process import AiGeneratedText


def parse_gemini_response(response: str) -> Tuple[AiGeneratedText, str]:
    try:
        clean_result = response.strip("```json").strip("```").strip()
        print(f'clean_result {clean_result} & {type(clean_result)}')
        parsed_data = json.loads(clean_result)

        print(f'parsed_data {parsed_data}')
        diagnosis = parsed_data.get("diagnosis", "No diagnosis found.")
        treatment = parsed_data.get("treatment", "No treatment found.")
        doctors_recommended = parsed_data.get("doctors_recommended", [])
        suggestions = parsed_data.get("suggestions", [])

        formatted_response = (
            f"Diagnosis: {diagnosis}\n"
            f"Treatment: {treatment}\n"
            f"Doctors Recommended: {', '.join(doctors_recommended) if doctors_recommended else 'No doctors recommended.'}\n"
            f"suggestions: {', '.join(suggestions) if suggestions else 'No suggestions recommended.'}"
        )

        return AiGeneratedText(diagnosis=diagnosis, treatment=treatment,
                               doctors_recommended=doctors_recommended, suggestions=suggestions), formatted_response

    except json.JSONDecodeError as e:
        error_message = f"Error parsing response: {str(e)}"
        return AiGeneratedText(diagnosis="", treatment="", doctors_recommended=[], suggestions=[]), error_message
