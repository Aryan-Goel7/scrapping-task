from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from celery.result import AsyncResult
from .tasks import scrapping_task
import json


class ScrapperList(APIView):

    def get(self, request, format=None) -> Response:
        task_id = request.query_params.get('task_id')
        if not task_id:
            return Response({'error': 'task_id query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        task_result = AsyncResult(task_id)
        if task_result.ready():
            result = task_result.result
            try:
                return Response({'status': 'completed', 'data': result})
            except json.JSONDecodeError:
                return Response({'error': 'Failed to decode JSON result'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'status': 'pending'})

    def post(self, request: Request, format=None) -> Response:
        data = json.loads(request.body) 
        coins_name = data.get('coins_name')
        if coins_name:
            task_id = scrapping_task.delay(coins_name).id
            return Response({"task_id": task_id}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "coin_name not provided"}, status=status.HTTP_400_BAD_REQUEST)
