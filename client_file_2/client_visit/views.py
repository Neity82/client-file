import datetime
from itertools import chain

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView

from client_visit.forms import VisitForm, VisitNameForm, CallForm
from client_visit.models import ClientVisit, ClientCall
from client_visit.utils import client_normalize

TODAY = datetime.date.today()


class IndexView(ListView):
    """Представление главной страницы"""

    model = ClientVisit
    template_name = 'client_visit/index.html'
    context_object_name = 'potential'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page'] = 'potential'
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            start = TODAY
            end = start + datetime.timedelta(days=14)
            visits_res = list()
            calls_res = list()

            if self.request.user.groups.filter(
                    name__in=['Фронт', 'Директор']
            ).exists():
                visits = ClientVisit.objects.filter(
                    employee__office=self.request.user.office,
                    credit_result='Планирует оформить',
                    date_next_contact__range=[start, end]
                )
                visits_res = visits.values(
                    'employee_id',
                    'date_next_contact'
                ).annotate(
                    sum=Sum('credit_sum'),
                    count=Count('credit_sum')
                )
                calls = ClientCall.objects.filter(
                    employee__office=self.request.user.office,
                    main_product='Кредит наличными',
                    result='Планирует оформить',
                    date_next_contact__range=[start, end]
                )
                calls_res = calls.values(
                    'employee_id',
                    'date_next_contact'
                ).annotate(
                    sum=Sum('sum'),
                    count=Count('result')
                )

            elif self.request.user.groups.filter(
                    name='Управляющий'
            ).exists():
                visits = ClientVisit.objects.filter(
                    credit_result='Планирует оформить',
                    date_next_contact__range=[start, end]
                )
                visits_res = visits.values(
                    'employee_id',
                    'date_next_contact'
                ).annotate(
                    sum=Sum('credit_sum'),
                    count=Count('credit_sum')
                )
                calls = ClientCall.objects.filter(
                    main_product='Кредит наличными',
                    result='Планирует оформить',
                    date_next_contact__range=[start, end]
                )
                calls_res = calls.values(
                    'employee_id',
                    'date_next_contact'
                ).annotate(
                    sum=Sum('sum'),
                    count=Count('result')
                )
            result_list = list(chain(visits_res, calls_res))
            total_data = []

            for i in result_list:
                if len(total_data) > 0:
                    for j in total_data:
                        if j['employee_id'] == i['employee_id'] and \
                                j['date_next_contact'] == i['date_next_contact']:
                            ind = total_data.index(j)
                            total_data[ind]['sum'] += i['sum']
                            total_data[ind]['count'] += i['count']
                            break
                    else:
                        total_data.append(i)
                else:
                    total_data.append(i)

            return total_data


class TaskTodayView(ListView):
    """Представление страницы задач на день"""

    paginate_by = 30
    model = ClientVisit
    template_name = 'client_visit/index.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page'] = 'tasks'
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            today_and_3_days = TODAY + datetime.timedelta(days=3)
            visit_today = None
            call_today = None

            if self.request.user.groups.filter(name='Фронт').exists():
                visit_today = ClientVisit.objects.filter(
                    date_next_contact__range=[TODAY, today_and_3_days],
                    employee=self.request.user
                ).select_related(
                    'employee'
                ).order_by(
                    'type_next_contact'
                )
                call_today = ClientCall.objects.filter(
                    date_next_contact__range=[TODAY, today_and_3_days],
                    employee=self.request.user
                ).select_related(
                    'employee'
                ).order_by(
                    'type_next_contact'
                )

            elif self.request.user.groups.filter(name='Директор').exists():
                visit_today = ClientVisit.objects.filter(
                    date_next_contact__range=[TODAY, today_and_3_days],
                    employee__office=self.request.user.office
                ).order_by(
                    'employee',
                    'type_next_contact'
                ).select_related(
                    'employee'
                )
                call_today = ClientCall.objects.filter(
                    date_next_contact__range=[TODAY, today_and_3_days],
                    employee__office=self.request.user.office
                ).order_by(
                    'employee',
                    'type_next_contact'
                ).select_related(
                    'employee'
                )
            elif self.request.user.groups.filter(name='Управляющий').exists():
                visit_today = ClientVisit.objects.filter(
                    date_next_contact__range=[TODAY, today_and_3_days],
                ).order_by(
                    'employee__office',
                    'employee',
                    'type_next_contact'
                ).select_related(
                    'employee'
                )
                call_today = ClientCall.objects.filter(
                    date_next_contact__range=[TODAY, today_and_3_days],
                ).order_by(
                    'employee__office',
                    'employee',
                    'type_next_contact'
                ).select_related(
                    'employee'
                )

            result_list = list(chain(visit_today, call_today))

            return result_list


class VisitTodayView(ListView):
    """Представление страницы визиты клиентов за день"""

    paginate_by = 30
    model = ClientVisit
    template_name = 'client_visit/index.html'
    context_object_name = 'visits'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page'] = 'visits'
        return context

    def get_queryset(self):
        visits_today = None
        if self.request.user.groups.filter(name='Фронт').exists():
            visits_today = ClientVisit.objects.filter(
                date_visit=TODAY,
                employee=self.request.user
            ).select_related(
                'employee'
            ).order_by(
                'type_next_contact'
            )

        elif self.request.user.groups.filter(name='Директор').exists():
            visits_today = ClientVisit.objects.filter(
                date_visit=TODAY,
                employee__office=self.request.user.office
            ).order_by(
                'employee'
            ).select_related(
                'employee'
            )

        elif self.request.user.groups.filter(name='Управляющий').exists():
            visits_today = ClientVisit.objects.filter(
                date_visit=TODAY
            ).order_by(
                'employee__office',
                'employee',
                'type_next_contact'
            ).select_related(
                'employee'
            )

        return visits_today


class CallTodayView(ListView):
    """Представление страницы звонки за день"""

    paginate_by = 30
    model = ClientCall
    template_name = 'client_visit/index.html'
    context_object_name = 'calls'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page'] = 'calls'
        return context

    def get_queryset(self):
        today = datetime.date.today()
        calls_today = None
        if self.request.user.groups.filter(name='Фронт').exists():
            calls_today = ClientCall.objects.filter(
                date_call=today,
                employee=self.request.user
            ).select_related(
                'employee'
            )

        elif self.request.user.groups.filter(name='Директор').exists():
            calls_today = ClientCall.objects.filter(
                date_call=today,
                employee__office=self.request.user.office
            ).order_by(
                'employee'
            ).select_related(
                'employee'
            )

        elif self.request.user.groups.filter(name='Управляющий').exists():
            calls_today = ClientCall.objects.filter(
                date_call=today
            ).order_by(
                'employee__office',
                'employee',
                'type_next_contact'
            ).select_related(
                'employee'
            )

        return calls_today


class VisitView(LoginRequiredMixin, CreateView):
    """Представление страницы первоначальное оформления визита клиента"""

    form_class = VisitNameForm
    template_name = 'client_visit/visit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Визит клиента'
        return context

    def form_valid(self, form):
        employee = self.request.user

        client = client_normalize(form.cleaned_data['name_client']).split()
        last_name_client = client[0]
        first_name_client = client[1]
        middle_name_client = client[2]
        date_of_birth = form.cleaned_data['date_of_birth']
        inn_employer = form.cleaned_data['inn_employer']
        main_product = form.cleaned_data['main_product']

        visit = ClientVisit.objects.create(
            employee=employee,
            last_name_client=last_name_client,
            first_name_client=first_name_client,
            middle_name_client=middle_name_client,
            date_of_birth=date_of_birth,
            inn_employer=inn_employer,
            main_product=main_product
        )
        # messages.success(self.request, 'Сохранено')

        return HttpResponseRedirect(reverse('visit_form', kwargs={'pk': visit.pk}))


class VisitFormView(LoginRequiredMixin, UpdateView):
    """Представление страницы детальное оформление визита клиента"""

    model = ClientVisit
    form_class = VisitForm
    template_name = 'client_visit/visit_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = self.object.last_name_client
        return context

    def form_valid(self, form):
        visit = form.save(commit=False)
        visit.save()
        messages.success(self.request, 'Запись сохранена', extra_tags=visit.pk)
        return HttpResponseRedirect(reverse('visit_form', kwargs={'pk': visit.pk}))


class VisitDetailView(LoginRequiredMixin, DetailView):
    """Представление страницы визит клиента"""

    model = ClientVisit
    template_name = 'client_visit/visit_detail.html'
    context_object_name = 'visits'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = self.object.last_name_client
        return context


class CallView(LoginRequiredMixin, CreateView):
    """Представление страницы первоначальное оформления звонка клиенту"""

    form_class = CallForm
    template_name = 'client_visit/call.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Звонок клиенту'
        return context

    def form_valid(self, form):
        form.instance.employee = self.request.user
        call = form.save()

        return HttpResponseRedirect(reverse('call_form', kwargs={'pk': call.pk}))


class CallFormView(LoginRequiredMixin, UpdateView):
    """Представление страницы детального заполнения звонка клиенту"""

    model = ClientCall
    form_class = CallForm
    template_name = 'client_visit/call_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = f'{self.object.last_name_client} ' \
                           f'{self.object.first_name_client} ' \
                           f'{self.object.middle_name_client}'
        return context

    def form_valid(self, form):
        call = form.save(commit=False)
        call.save()
        messages.success(self.request, 'Запись сохранена', extra_tags=call.pk)
        return HttpResponseRedirect(reverse('call_form', kwargs={'pk': call.pk}))


class CallDetailView(LoginRequiredMixin, DetailView):
    """Представление страницы звонка клиенту"""

    model = ClientCall
    template_name = 'client_visit/call_detail.html'
    context_object_name = 'calls'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = self.object.last_name_client
        return context
