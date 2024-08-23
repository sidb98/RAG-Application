from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .query_rag import query_rag
from .database import update_chroma, delete_file_from_chroma
import os
import json
from django.conf import settings
from django.core.files.storage import default_storage


@csrf_exempt
def query_view(request):
    if request.method == 'POST':
        try:
            # Parse the JSON body
            body = json.loads(request.body.decode('utf-8'))
            query_string = body.get('query_string')

            if not query_string:
                return HttpResponseBadRequest("Missing 'query_string' parameter")

            # Call your query function
            response = query_rag(query_string)
            return JsonResponse({"response_text": response["response_text"], "sources": response["sources"]})

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")
        except Exception as e:
            return HttpResponseBadRequest(str(e))

    return HttpResponseBadRequest("Invalid request method")

@csrf_exempt
def upload_file_view(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        if file.content_type != 'application/pdf':
            return HttpResponseBadRequest("Only PDF files are allowed")

        pdf_data_path = os.getenv("PDF_DATA_PATH")
        persist_directory_db_path = os.getenv("PERSIST_DIRECTORY_DB_PATH")

        if not os.path.exists(persist_directory_db_path):
            os.makedirs(persist_directory_db_path, exist_ok=True)

        try:
            file_location = os.path.join(pdf_data_path, file.name)
            os.makedirs(pdf_data_path, exist_ok=True)
            with default_storage.open(file_location, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            update_chroma()
        except Exception as e:
            return HttpResponseBadRequest(str(e))

        return JsonResponse({"filename": file.name, "detail": "File processed and added to Chroma successfully"})
    return HttpResponseBadRequest("Invalid request")

# backend/views.py

def get_files_view(request):
    if request.method == "GET":
        try:
            pdf_data_path = settings.PDF_DATA_PATH
            print(f"PDF_DATA_PATH: {pdf_data_path}")
            
            if not os.path.exists(pdf_data_path):
                print(f"Directory {pdf_data_path} does not exist.")
                return JsonResponse({"error": f"Directory {pdf_data_path} does not exist."}, status=400)

            files = os.listdir(pdf_data_path)
            print(f"Files found: {files}")
            return JsonResponse({"files": files})
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def delete_file_view(request):
    if request.method == 'POST':
        try:
            # Parse the JSON body
            body = json.loads(request.body.decode('utf-8'))
            prefix = body.get('prefix')

            if not prefix:
                return HttpResponseBadRequest("Missing 'prefix' parameter")

            # Call your delete function
            delete_file_from_chroma(prefix)
            return JsonResponse({"detail": f"Documents with prefix '{prefix}' removed successfully"})

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")
        except Exception as e:
            return HttpResponseBadRequest(str(e))

    return HttpResponseBadRequest("Invalid request method")
