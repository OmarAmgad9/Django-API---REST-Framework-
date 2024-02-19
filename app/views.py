from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly
from .models import Post
from .serializers import PostSerializer
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
    try:
        guest = Guest.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # GET
    if request.method == 'GET':
        print(guest)
        serializer = GuestSerializer(guest)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = GuestSerializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)



#4 CBV Class Based Views
from rest_framework.views import APIView
#4.1 List == GET and Create == Post
class CVB_List(APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
#4.2 GET With key or put or delete
from django.http import Http404
class  CBV_pk(APIView):

    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404
    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#5 Mixins 
from rest_framework import generics, mixins, viewsets

    #5.1
class Mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    
    def get(self, request):
        return self.list(request)
    def post(self, request):
        return self.create(request)
    #5.2
class Mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    def get(self, request):
        return self.retrieve(request)
    def put(self, request):
        return self.update(request)
    def delete(self, request):
        return self.destroy(request)
#6 Generics
    #6.1 

class Generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]


    #6.2
class Generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    # authentication_classes = [TokenAuthentication]

#7 ViewSets
class ViweSets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie']

class ViewSets_moive(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class ViewSets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

#8 Find Movie 
@api_view(['GET'])
def find_movie(request):
    movie = Movie.objects.filter(movie=request.data['movie'] )
    serializer = MovieSerializer(movie, many=True)
    return Response(serializer.data)
@api_view(['POST'])
def new_reservation(request):
    movie = Movie.objects.get(movie=request.data['movie'])
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['moblie']
    guest.save()
    reservation =  Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()
    serializer = ReservationSerializer(reservation)
    return Response(serializer.data,status=status.HTTP_201_CREATED)

#9 Create New Reservation

#10 Post Author Editor
class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer