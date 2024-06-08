from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from celery.result import AsyncResult
from .tasks import scrapping_task
import json


class ScrapperList(APIView):
    
    def get(self, request: Request, format=None):
        task_id = request.query_params.get('task_id')
        if not task_id:
            return Response({'error': 'task_id query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        task_result = AsyncResult(task_id)
        if task_result.ready():
            result = task_result.result
            result_json = json.loads(result)
            return Response({'status': 'completed', 'result': result_json})
        else:
            return Response({'status': 'pending'})

    def post(self, request: Request, format=None):
        
        data = request.data

        
        coin_name = data.get('coin_name')

        if coin_name:
            task_id = scrapping_task.delay(coin_name).id
            return Response({"task_id": task_id}, status=status.HTTP_200_OK)
        else:
            # Return an error response if coin_name is not provided
            return Response({"error": "coin_name not provided"}, status=status.HTTP_400_BAD_REQUEST)