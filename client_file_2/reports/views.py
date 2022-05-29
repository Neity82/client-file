import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import TemplateView, ListView

from client_visit.models import ClientVisit, ClientCall
from reports.forms import FilterInReports
from reports.utils import get_month_name, get_quarter


class ReportsView(LoginRequiredMixin, TemplateView):
    """Представление страницы со списком отчетов"""

    template_name = 'reports/reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Отчеты'
        return context


class SalesReportsDayView(LoginRequiredMixin, TemplateView):
    """Представление страницы отчет за текущий день"""

    template_name = 'reports/today_sales_reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Продажи за день'
        context['today'] = datetime.date.today()
        return context


class SalesReportsMonthView(LoginRequiredMixin, TemplateView):
    """Представление страницы отчет за месяц"""

    template_name = 'reports/month_sales_reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Продажи за месяц'
        context['month'] = get_month_name(datetime.date.today().month)
        return context


class SalesReportsQuarterView(LoginRequiredMixin, TemplateView):
    """Представление страницы отчет за квартал"""

    template_name = 'reports/quarter_sales_reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Продажи за квартал'
        context['quarter'] = get_quarter(datetime.date.today().month)
        return context


class VisitDetailReportsView(LoginRequiredMixin, ListView):
    """Представление страницы визиты"""

    paginate_by = 30
    model = ClientVisit
    template_name = 'reports/visit_detail_reports.html'
    context_object_name = 'visits'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Детализация визитов'
        context['filter'] = FilterInReports()
        return context

    def get_queryset(self):
        result = None
        if self.request.user.groups.filter(name='Фронт').exists():
            result = ClientVisit.objects.filter(employee=self.request.user)
        elif self.request.user.groups.filter(name='Директор').exists():
            result = ClientVisit.objects.filter(
                employee__office=self.request.user.office
            ).order_by(
                '-date_visit',
                'employee'
            )
        elif self.request.user.groups.filter(name='Управляющий').exists():
            result = ClientVisit.objects.all().order_by(
                '-date_visit',
                'employee__office',
                'employee'
            )
        return result


class CallDetailReportsView(LoginRequiredMixin, ListView):
    """Представление страницы звонков"""

    paginate_by = 30
    model = ClientCall
    template_name = 'reports/call_detail_reports.html'
    context_object_name = 'calls'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Детализация звонков'
        context['filter'] = FilterInReports()
        return context

    def get_queryset(self):
        result = None
        if self.request.user.groups.filter(name='Фронт').exists():
            result = ClientCall.objects.filter(
                employee=self.request.user
            )
        elif self.request.user.groups.filter(name='Директор').exists():
            result = ClientCall.objects.filter(
                employee__office=self.request.user.office
            ).order_by(
                '-date_call',
                'employee'
            )
        elif self.request.user.groups.filter(name='Управляющий').exists():
            result = ClientCall.objects.all().order_by(
                '-date_call',
                'employee__office',
                'employee'
            )
        return result


class FilterVisitsView(LoginRequiredMixin, ListView):
    paginate_by = 30
    template_name = 'reports/visit_detail_reports.html'
    context_object_name = 'visits'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Фильтр'
        context['filter'] = FilterInReports()
        return context

    def get_queryset(self):
        queryset = ClientVisit.objects.filter(
            Q(credit_result=self.request.GET.get("result")) |
            Q(credit_card_result=self.request.GET.get("result")) |
            Q(deposit_result=self.request.GET.get("result")) |
            Q(service_package_result=self.request.GET.get("result")) |
            Q(izp_result=self.request.GET.get("result")) |
            Q(pension_result=self.request.GET.get("result")) |
            Q(ksp_result=self.request.GET.get("result")) |
            Q(nsg_result=self.request.GET.get("result")) |
            Q(isg_result=self.request.GET.get("result")) |
            Q(npo_result=self.request.GET.get("result"))
        )
        return queryset


class FilterCallsView(LoginRequiredMixin, ListView):
    paginate_by = 30
    template_name = 'reports/call_detail_reports.html'
    context_object_name = 'calls'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Фильтр'
        context['filter'] = FilterInReports()
        return context

    def get_queryset(self):
        queryset = ClientCall.objects.filter(
            result=self.request.GET.get("result")
        )
        return queryset
