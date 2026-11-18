from .serializers import PythonFileSerializer
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .analyzer import analyze_python_file


@api_view(['GET'])
def home(request):

    return Response({
        "project": "COGNIVEX AI",
        "message": "Welcome to Cognivex AI Backend!",
        "status": "Backend is running successfully",
        "version": "1.0"
    })


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_file(request):

    uploaded_file = request.FILES.get('file')

    if not uploaded_file:
        return Response(
            {"error": "Please select a Python file"},
            status=400
        )

    if not uploaded_file.name.lower().endswith('.py'):
        return Response(
            {"error": "Only Python files are allowed"},
            status=400
        )

    if uploaded_file.size > 5 * 1024 * 1024:
        return Response(
            {"error": "File size must be below 5 MB"},
            status=400
        )

    # Read uploaded source code without executing it
    try:
        source_code = uploaded_file.read().decode("utf-8")
    except UnicodeDecodeError:
        return Response(
            {"error": "File must contain valid UTF-8 text"},
            status=400
        )

    # Save uploaded file
    storage = FileSystemStorage(
        location=settings.BASE_DIR / "uploaded_files"
    )

    uploaded_file.seek(0)
    saved_name = storage.save(uploaded_file.name, uploaded_file)

    # Analyse uploaded code
    try:
        result = analyze_python_file(source_code)

    except Exception as error:
        return Response({
            "message": "File uploaded, but analysis failed",
            "file_name": saved_name,
            "error": str(error)
        }, status=500)

    return Response({
        "message": "File uploaded and analysed successfully",
        "file_name": saved_name,
        "analysis": result
    }, status=201)
