import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google import genai
from google.genai import types
from backend_api.function import *

# Set up logging
logger = logging.getLogger(__name__)

# File paths for reading and writing
file_path = pathgetter('systeminstruction.txt')
qa_path = pathgetter('qainstruction.txt')
prompt_path = pathgetter('promt.txt')
response_path = pathgetter('response.txt')
system_path = pathgetter('questioninstruction.txt')
answer_path = pathgetter('answerinstruction.txt')
pa_path = pathgetter('prompta.txt')
@csrf_exempt
def generate_text(request):
    if request.method == "POST":
        system_content = reader(file_path)
        prompt_content = reader(prompt_path)

        client = genai.Client(api_key='AIzaSyDsqllXdHi4MwFskfrIpaNOfMNOc4Yphhk')
        body = json.loads(request.body)
        grade = body.get("grade")
        location = body.get("location")
        subject = body.get("subject")

        prompt = prompt_content.format(grade=grade, location=location, subject=subject)
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
    if request.method == "POST":
        system_content = reader(qa_path)
        client = genai.Client(api_key='AIzaSyDsqllXdHi4MwFskfrIpaNOfMNOc4Yphhk')

        body = json.loads(request.body)
        prompt = body.get('question', '')

        if not prompt:
            return JsonResponse({'error': 'No question provided.'}, status=400)

        result = client.models.generate_content(
            config=types.GenerateContentConfig(
                system_instruction=system_content
            ),
            model="gemini-2.0-flash",
            contents=[prompt]
        )

        try:
            response_text = result.candidates[0].content.parts[0].text
        except (AttributeError, IndexError):
            return JsonResponse({'error': 'Failed to generate content.'}, status=500)

        return JsonResponse({'response': response_text})
    else:
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)
# end of <---------- part 2 start of part 3 ----------------->
@csrf_exempt
def check_answers(request):
    if request.method == "POST":
        system_content = reader(answer_path)
        prompt_content = reader(pa_path)

        client = genai.Client(api_key='AIzaSyDsqllXdHi4MwFskfrIpaNOfMNOc4Yphhk')
        body = json.loads(request.body)
        question = body.get("question")
        answer = body.get("answer")

        prompt = prompt_content.format(question=question, answer = answer)
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