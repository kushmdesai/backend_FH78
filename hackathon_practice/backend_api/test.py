from django.http import HttpResponse
from . import function
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

@csrf_exempt
def test_view(request):
    try:
        path = function.pathgetter('response.json')
        text = function.reader(path)
        try:
            response_data = json.loads(text)  # this makes sure you're sending a Python dict
            return JsonResponse(response_data)
        except json.JSONDecodeError as e:
            return JsonResponse({"error": f"JSON decode failed: {str(e)}"}, status=500)

        return HttpResponse(f"File content:<br><pre>{text}</pre>")
    except FileNotFoundError:
        return HttpResponse("response.txt not found.", status=404)
