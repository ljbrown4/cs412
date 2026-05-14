from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.ResultsListView.as_view(), name='mar_home'),
    path(r'results', views.ResultsListView.as_view(), name='results_list'),
    path(r'result/<int:pk>', views.ResultDetailView.as_view(), name='result_detail')
]