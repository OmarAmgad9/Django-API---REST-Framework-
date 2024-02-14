from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):

    return HttpResponse("Hello World")


# 1 without REST and no Query
from django.http.response import JsonResponse
def no_rest_no_model(request):
    guests = [
        {
            'id': 1,
            'Name': "Omar",
            'mobile': 2939449,
        },
        {
            'id': 2,
            'Name': "Yassin",
            'mobile': 2939449,
        },
    ]
    return JsonResponse(guests, safe=False)



#2 model data Defaul django without REST
from .models import Guest, Movie, Reservation
def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {
        'guests': list(data.values('name', 'mobile'))
    }
    return JsonResponse(response)

#3 Function Based Views
#3.1 GET POST
from rest_framework.decorators import api_view
from .serializers import GuestSerializer, ReservationSerializer, MovieSerializer
from rest_framework.response import Response
from rest_framework import status, filters
@api_view(['GET', 'POST'])
def FBV_List(request):

    #GET
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    # POST
    elif request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def FBV_pk(request, pk):

    guest = Guest.objects.get(pk=pk)
    # GET
    if request.method == 'GET':
        print(guest)
        serializer = GuestSerializer(guest)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    return Response(status=status.HTTP_400_BAD_REQUEST)
