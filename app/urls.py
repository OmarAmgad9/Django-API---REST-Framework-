from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    # 1
    path('jsonresponsenomodels', views.no_rest_no_model),
    # 2
    path('jsonresposnsewithmodels', views.no_rest_from_model),
    # 3 
        #3.1
        path('functionBaseViewsList', views.FBV_List),
        # 3.2
        path('functionBaseViewPk/<int:pk>', views.FBV_pk)
]
