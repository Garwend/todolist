from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Task
from .serializer import TaskSerializer


def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        ip = x_forwarded.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class TasksList(APIView):

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data

        is_done_key_exist = 'done' in data
        is_done_date_key_exist = 'done_date' in data

        if is_done_key_exist and data['done'] == False and is_done_date_key_exist and data['done_date'] != None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskSerializer(data=data)

        if serializer.is_valid():
            if is_done_key_exist and data['done'] == True and not is_done_date_key_exist:
                serializer.save(author_ip=get_client_ip(
                    request), done_date=timezone.now())
            else:
                serializer.save(author_ip=get_client_ip(request))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetail(APIView):

    def get(self, request, id):
        task = get_object_or_404(Task, id=id)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        task = get_object_or_404(Task, id=id)
        task.delete()
        return Response(status=status.HTTP_200_OK)
