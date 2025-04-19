import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google import genai
from google.genai import types
from backend_api.function import *

# File paths for reading and writing
file_path = pathgetter('systeminstruction.txt')
promt_path = pathgetter('promt.txt')
response_path = pathgetter('response.txt')
system_path = pathgetter('questioninstruction.txt')

@csrf_exempt
def generate_text(request):
    if request.method == "POST":
        system_content = reader(file_path)
        promt_content = reader(promt_path)

        client = genai.Client(api_key=process.env.GOOGLE_API_KEY)
        body = json.loads(request.body)
        grade = body.get("grade")
        location = body.get("location")
        subject = body.get("subject")

        prompt = promt_content.format(grade=grade, location=location, subject=subject)
        result = client.models.generate_content(
            config=types.GenerateContentConfig(
                system_instruction=system_content
            ),
            model="gemini-2.0-flash",
            contents=[prompt]
        )

        print(f"obtained response = {result.text}")
        writer(response_path, result.text)

        # Clean and validate
        editor_response()

        # Read and parse for Django's JsonResponse
        cleaned_text = reader(response_path)

        try:
            response_data = json.loads(cleaned_text)  # this makes sure you're sending a Python dict
            return JsonResponse(response_data)
        except json.JSONDecodeError as e:
            return JsonResponse({"error": f"JSON decode failed: {str(e)}"}, status=500)

    return JsonResponse({"error": "Only POST allowed"}, status=405)

# end of <-----first part second part start here-------->
@csrf_exempt
def generate_questions(request):
    system_content = reader(system_path)
    client = genai.Client(api_key=process.env.GOOGLE_API_KEY)
    body = json.loads(request.body)
    promt = body.get("question")
    result = client.models.generate_content(
            config=types.GenerateContentConfig(
                system_instruction=system_content
            ),
            model="gemini-2.0-flash",
            contents=[promt]
        )
    print(f"obtained response = {result.text}")
    return JsonResponse({"answer":result.text})