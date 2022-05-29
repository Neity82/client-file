from django.urls import path

from client_visit.views import IndexView, VisitView, VisitFormView, VisitDetailView, \
    CallView, CallFormView, CallDetailView, VisitTodayView, CallTodayView, TaskTodayView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('index/tasks_today/', TaskTodayView.as_view(), name='tasks_today'),
    path('index/visits_today/', VisitTodayView.as_view(), name='visits_today'),
    path('index/calls_today/', CallTodayView.as_view(), name='calls_today'),
    path('visit/', VisitView.as_view(), name='visit'),
    path('visit/<int:pk>', VisitFormView.as_view(), name='visit_form'),
    path('call/', CallView.as_view(), name='call'),
    path('call/<int:pk>', CallFormView.as_view(), name='call_form'),
    path('visit/detail/<int:pk>', VisitDetailView.as_view(), name='visit_detail'),
    path('call/detail/<int:pk>', CallDetailView.as_view(), name='call_detail'),

]
