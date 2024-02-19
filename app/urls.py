from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
router = DefaultRouter()
router.register('guests', views.ViweSets_guest)
router.register('movie', views.ViewSets_moive)
router.register('reservation', views.ViewSets_reservation)

urlpatterns = [
    path('', views.home),
    # 1
    path('jsonresponsenomodels', views.no_rest_no_model),
    # 2
    path('jsonresposnsewithmodels', views.no_rest_from_model),
    # 3 function base views 
        #3.1
        path('functionBaseViewsList', views.FBV_List),
        # 3.2
        path('functionBaseViewPk/<int:pk>', views.FBV_pk),
    #4 class base views
        #4.1
        path('classBaseviewslist', views.CVB_List.as_view()),
        #4.2
        path('classBaseviewpk/<int:pk>', views.CBV_pk.as_view()),
    #5
        #5.1 mixins
        path('mixins', views.Mixins_list.as_view()),
        #5.2 minxins
        path('mixins_pk', views.Mixins_pk.as_view()),
    #6 Generics
        #6.1 
        path('generics',views.Generics_list.as_view()),
        #6.2
        path('generics_pk',views.Generics_pk.as_view()),
    #7 ViewSets
        path('viewsets/', include(router.urls)),
    #8 Find Movie
    path('findmovie', views.find_movie),
    #9 New Resevartion
    path('newresvation', views.new_reservation),

    #10
    path('api-auth', include('rest_framework.urls')),

    #11 Token Authentication
    # to generat token
    path('api-token', obtain_auth_token)
    #12 Post Pk Generics
    ,path('postgenrics/<int:pk>', views.Post_pk.as_view())
]
