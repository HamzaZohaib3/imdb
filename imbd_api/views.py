from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework import mixins
from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework import viewsets

# Create your views here.
@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "watchlist": reverse("movie_list", request=request, format=format),
            "streamplatform": reverse("stream_list", request=request, format=format),
        }
    )


@api_view(["GET"]) 
def movie_list(request,formate = None):
    moive_list = watchlist.objects.all()
    serializer = watchlistserializer(moive_list, many = True)
    return Response(serializer.data)

@api_view(["GET"])
def movie_detail(request,pk,formate = None):
    moive = watchlist.objects.get(pk=pk)
    serializer = watchlistserializer(moive)
    return Response(serializer.data)

class streamplatformViewSet(viewsets.ModelViewSet):
    queryset = streamplatform.objects.all()
    serializer_class = streamplatformserializer
    


# class stream_list(generics.ListCreateAPIView):
#     queryset = streamplatform.objects.all()
#     serializer_class = streamplatformserializer


# class stream_detail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = streamplatform.objects.all()
#     serializer_class = streamplatformserializer

# class stream_list(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = streamplatform.objects.all()
#     serializer_class = streamplatformserializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    
# class stream_detail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
#     queryset = streamplatform.objects.all()
#     serializer_class = streamplatformserializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# class stream_list(APIView):
#     def get(self, request, formate = None):
#         stream_list = streamplatform.objects.all()
#         serializer = streamplatformserializer(stream_list, many = True)
#         return Response(serializer.data)
    
    
#     def post(self, request, formate = None):
#         serializer = streamplatformserializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    
# class stream_detail(APIView):
#     def get_object(request,pk):
#         try:
#             return streamplatform.objects.get(pk=pk)
#         except:
#             return Response(status= status.HTTP_404_NOT_FOUND)
        
#     def get(self, request, pk, formate = None):
#         streamplatform = self.get(pk)
#         serializer = streamplatformserializer(streamplatform)
#         return Response(serializer.data)
    
#     def put(self, request, pk, formate = None):
#         streamplatform = self.get(pk)
#         serializer = streamplatformserializer(streamplatform, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk, formate = None):
#         streamplatform = self.get(pk)
#         streamplatform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        
        
        
        
# @api_view(["GET", "POST"])
# def stream_list(request):
    
#     if request.method == 'GET':
#         stream_list = streamplatform.objects.all()
#         serializer = streamplatformserializer(stream_list, many = True)
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = streamplatformserializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# @api_view(["GET", "PUT", "DELETE"])
# def stream_detail(request,pk):
#     try:
#         stream = streamplatform.objects.get(pk=pk)
#     except:
#         return Response(status= status.HTTP_404_NOT_FOUND)
    
#     if request.method == "GET":
#         serializer = streamplatformserializer(stream)
#         return Response(serializer.data)

#     elif request.method == "PUT":
#         serializer = streamplatformserializer(stream, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == "DELETE":
#         streamplatform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
    