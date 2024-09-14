from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer, UserSerialzier
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema # سواگر تو این هست گه باید نصب کنی



User = get_user_model()


# به همه روش های زیر میشه عملیات crud رو انجام داد

#region function base view

# CRUD
@api_view(['GET', 'POST'])
def all_todos(request: Request):
    if request.method == 'GET':
        todos = Todo.objects.order_by('priority').all()
        todo_serializer = TodoSerializer(todos, many=True)
        return Response(todo_serializer.data, status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
    
    return Response(None, status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail_view(request: Request, todo_id: int):
    try:
        todo = Todo.objects.get(pk=todo_id)
    except Todo.DoesNotExist:
        return Response(None, status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_202_ACCEPTED)
        return Response(None, status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        todo.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)


# endregion

# region class base view

class TodosListApiView(APIView):
    # برای قشنگ شدن سواگر هست
    @extend_schema(
        # نشون دادن نمونه ریسپاس
        request=TodoSerializer,
        responses={201: TodoSerializer},
        description='this api is used for get all todos list',
    )
    def get(self, request: Request):
        todos = Todo.objects.order_by('priority').all()
        todo_serializer = TodoSerializer(todos, many=True)
        return Response(todo_serializer.data, status.HTTP_200_OK)
    
    def post(self, request: Request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(None, status.HTTP_400_BAD_REQUEST)


class TodosDetailApiView(APIView):
    
    def get_object(self, todo_id: int):
        try:
            todo = Todo.objects.get(pk=todo_id)
            return todo
        except Todo.DoesNotExist:
            return Response(None, status.HTTP_404_NOT_FOUND)
    
    def get(self, request: Request, todo_id: int):
        todo = self.get_object(todo_id)
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def put(self, request: Request, todo_id: int):
        todo = self.get_object(todo_id)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_202_ACCEPTED)
        return Response(None, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request: Request, todo_id: int):
        todo = self.get_object(todo_id)
        todo.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)


#endregion

#region mixins

class TodosListMixinApiView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    
    def get(self, request: Request):
        return self.list(request)
    
    def post(self, request: Request):
        return self.create(request)


class TodosDetailMixinApiView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                              generics.GenericAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    
    def get(self, request: Request, pk):
        return self.retrieve(request, pk)
    
    def put(self, request: Request, pk):
        return self.update(request, pk)
    
    def delete(self, request: Request, pk):
        return self.destroy(request, pk)


#endregion

#region generics

class TodosGenericApiViewPagination(PageNumberPagination):  # میشه هم این رو ننویسی و همون که ارث بری کردی رو پایین بزاری
    page_size = 3  #                                           دیفالتش توی تنظیمات هست


class TodosGenericApiView(generics.ListCreateAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    pagination_class = TodosGenericApiViewPagination  # اگه نزاری اونی که تو تنظیمات گزاشتی دیفالتش هست
    
    # authentication_classes = [BasicAuthentication] # نحوه اهراز هویت
    # permission_classes = [IsAuthenticated] # سطح دسترسی
    # اگه نزاری دیفالتش اونی که تو تظیمات زدی هست


class TodosGenericDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer


#endregion

#region viewsets
# این خودش سواگر رو عالی هندل میکنه

# با همین سه خط هر 5 کار رو انجام میده فقط url رو بباید جور دیگه ای ینویسی
class TodosViewSetApiView(viewsets.ModelViewSet):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    pagination_class = LimitOffsetPagination  # اگه نزاری اونی که تو تنظیمات گزاشتی دیفالتش هست


#endregion

#region users

class UsersGenericApiView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerialzier

#endregion
