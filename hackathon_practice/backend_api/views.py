import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google import genai

@csrf_exempt
def generate_text(request):
    if request.method == "POST":
        client = genai.Client(api_key=process.env.GOOGLE_API_KEY)
        body = json.loads(request.body)
        input_text = body.get("input_text")
        result = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[input_text],
            )
        return JsonResponse({"response": result.text})
    return JsonResponse({"error": "Only POST allowed"}, status=405)