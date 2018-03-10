from datetime import timedelta, time

from django import forms
from django.contrib.auth import authenticate, login, views as auth_views
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from django.views.generic import FormView, DetailView, UpdateView
from django.views.generic.edit import FormMixin

from connect_therapy.forms.patient import PatientSignUpForm, PatientLoginForm, \
    PatientNotesBeforeForm, PatientForm, PatientUserForm, PatientEditMultiForm
from connect_therapy import notifications
from connect_therapy.models import Patient, Appointment


class PatientSignUpView(FormView):
    form_class = PatientSignUpForm
    template_name = 'connect_therapy/patient/signup.html'
    success_url = reverse_lazy('connect_therapy:patient-login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.email
        user.save()
        patient = Patient(user=user,
                          date_of_birth=form.cleaned_data['date_of_birth'],
                          gender=form.cleaned_data['gender'],
                          mobile=form.cleaned_data['mobile']
                          )
        patient.save()
        user = authenticate(username=form.cleaned_data['email'],
                            password=form.cleaned_data['password1']
                            )
        login(request=self.request, user=user)
        return super().form_valid(form)


class PatientLoginView(auth_views.LoginView):
    template_name = 'connect_therapy/patient/login.html'
    authentication_form = PatientLoginForm

    def get_success_url(self):
        return reverse_lazy('connect_therapy:patient-homepage')


class PatientMyAppointmentsView(generic.TemplateView):
    template_name = 'connect_therapy/patient/my-appointments.html'

    model = Appointment

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['future_appointments'] = Appointment.objects.filter(
            start_date_and_time__gte=timezone.now(),
            patient=self.request.user.patient
        ).order_by('-start_date_and_time')
        context['past_appointments'] = Appointment.objects.filter(
            start_date_and_time__lt=timezone.now(),
            patient=self.request.user.patient
        ).order_by('-start_date_and_time')
        return context


class PatientNotesBeforeView(FormMixin, UserPassesTestMixin, DetailView):
    form_class = PatientNotesBeforeForm
    template_name = 'connect_therapy/patient/notes-before-appointment.html'
    success_url = reverse_lazy('connect_therapy:patient-my-appointments')
    login_url = reverse_lazy('connect_therapy:patient-my-appointments')
    redirect_field_name = None
    model = Appointment

    def test_func(self):
        return self.request.user.id == self.get_object().patient.user.id

    def form_valid(self, form):
        self.appointment.patient_notes_before_meeting = \
            form.cleaned_data['patient_notes_before_meeting']
        self.appointment.save()
        return super().form_valid(form)

    def post(self, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid()
        else:
            return self.form_invalid()


class PatientCancelAppointmentView(UserPassesTestMixin, FormMixin, DetailView):
    model = Appointment
    form_class = forms.Form
    template_name = 'connect_therapy/appointment_detail.html'
    login_url = reverse_lazy('connect_therapy:patient-my-appointments')
    redirect_field_name = None

    def test_func(self):
        return self.request.user.id == self.get_object().patient.user.id

    def get_success_url(self):
        return reverse_lazy('connect_therapy:patient-my-appointments')

    def get_context_data(self, **kwargs):
        context = super(PatientCancelAppointmentView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        # Here, we would record the user's interest using the message
        # passed in form.cleaned_data['message']
        notifications.appointment_cancelled_by_patient(
            self.object.patient,
            self.object,
            self.object.start_date_and_time < timezone.now() + timedelta(hours=24)
        )
        self.object.patient = None
        self.object.save()
        self.split_merged_appointment()

        return super(PatientCancelAppointmentView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid() and self.object.start_date_and_time > timezone.now():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def split_merged_appointment(self):
        original_length = self.object.length

        if original_length.minute == 30:
            return

        self.object.length = time(minute=30)
        self.object.patient = None
        number_of_appointments = \
            (original_length.hour * 60 + original_length.minute) // 30
        for i in range(1, number_of_appointments):
            appointment = Appointment(
                practitioner=self.object.practitioner,
                patient=None,
                length=time(minute=30),
                start_date_and_time=self.object.start_date_and_time
                                    + timedelta(minutes=30 * i)
            )
            appointment.save()
            self.object.save()


class PatientPreviousNotesView(UserPassesTestMixin, generic.DetailView):
    login_url = reverse_lazy('connect_therapy:patient-my-appointments')
    redirect_field_name = None
    model = Appointment
    template_name = 'connect_therapy/patient/appointment-notes.html'

    def test_func(self):
        return self.request.user.id == self.get_object().patient.user.id


class PatientProfile(LoginRequiredMixin, generic.TemplateView):
    template_name = 'connect_therapy/patient/profile.html'

    @login_required
    def view_profile(self, request):
        user = request.user
        args = {'user': user}
        return render(request, args)


class PatientEditDetailsView(UserPassesTestMixin,UpdateView):
    model = Patient
    template_name = 'connect_therapy/patient/edit-profile.html'
    form_class = PatientEditMultiForm
    success_url = reverse_lazy('connect_therapy:patient-profile')
    login_url = reverse_lazy('connect_therapy:patient-profile')
    redirect_field_name = None

    def test_func(self):
        return self.request.user.id == self.get_object().user.id

    def form_valid(self, form):
        self.object.user.username = form.cleaned_data['user']['email']
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        try:
            user = User.objects.get(username=form.cleaned_data['user']['email'])
            if form.is_valid():
                return self.form_valid(form)
        except User.DoesNotExist:
            # if User.objects.get(email=user.email) == user.email:
            #     return self.form_valid(form)
            if form.is_valid():
                return self.form_valid(form)

        return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(PatientEditDetailsView, self).get_form_kwargs()
        kwargs.update(instance={
            'user': self.object.user,
            'patient': self.object,
        })
        return kwargs
