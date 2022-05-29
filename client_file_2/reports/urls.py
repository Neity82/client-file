from django.urls import path

from reports.views import ReportsView, SalesReportsDayView, SalesReportsMonthView, SalesReportsQuarterView, \
    VisitDetailReportsView, CallDetailReportsView, FilterVisitsView, FilterCallsView

urlpatterns = [
    path('reports/', ReportsView.as_view(), name='reports'),
    path('filter/visits/', FilterVisitsView.as_view(), name='filter_visits'),
    path('filter/calls/', FilterCallsView.as_view(), name='filter_calls'),
    path('reports/sales_today/', SalesReportsDayView.as_view(), name='today_sales_reports'),
    path('reports/sales_month/', SalesReportsMonthView.as_view(), name='month_sales_reports'),
    path('reports/sales_quarter/', SalesReportsQuarterView.as_view(), name='quarter_sales_reports'),
    path('reports/visit_detail_reports/', VisitDetailReportsView.as_view(), name='visit_detail_reports'),
    path('reports/call_detail_reports/', CallDetailReportsView.as_view(), name='call_detail_reports'),

]
