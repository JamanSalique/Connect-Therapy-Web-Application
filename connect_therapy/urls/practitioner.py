from django.urls import path
from django.views.generic import TemplateView

from connect_therapy.views.practitioner import *

urlpatterns = [
    path('signup',
         PractitionerSignUpView.as_view(),
         name='practitioner-signup'
         ),
    path('signup/success',
         TemplateView.as_view(
             template_name='connect_therapy/practitioner/signup-success.html'
         ),
         name='practitioner-signup-success'
         ),
    path('login',
         PractitionerLoginView.as_view(),
         name='practitioner-login'
         ),
    path('login/success',
         TemplateView.as_view(
             template_name='connect_therapy/practitioner/login-success.html'
         ),
         name='practitioner-login-success'
         ),
    path('logout',
         auth_views.logout,
         {
             'next_page':
                 reverse_lazy('connect_therapy:index'),
         },
         name='practitioner-logout'
         ),
    path('logout/success',
         TemplateView.as_view(
             template_name='connect_therapy/practitioner/logout-success.html'
         ),
         name='practitioner-logout-success'
         ),
    path('',
         PractitionerHomepageView.as_view(),
         name='practitioner-homepage'
         ),
    path('make-notes/<int:pk>',
         PractitionerNotesView.as_view(),
         name='practitioner-make-notes'
         ),
    path('view-notes/<int:pk>',
         PractitionerPreviousNotesView.as_view(),
         name='practitioner-view-notes'
         ),
    path('my-appointments',
         PractitionerMyAppointmentsView.as_view(),
         name='practitioner-my-appointments'
         ),
    path('view-patients',
         PractitionerAllPatientsView.as_view(),
         name='practitioner-view-patients'
         ),
    path('profile',
         PractitionerProfile.as_view(),
         name='practitioner-profile'
         ),
    path('profile/edit/<int:pk>',
         PractitionerEditDetailsView.as_view(),
         name='practitioner-profile-edit'
         ),
    path('profile/change-password',
         change_password,
         name='practitioner-change-password'),
    path('set-appointments',
         PractitionerSetAppointmentView.as_view(),
         name='practitioner-set-appointments'
         ),
    path('cancel-appointment/<int:pk>',
         PractitionerAppointmentDelete.as_view(),
         name='practitioner-cancel-appointment'
         ),
]
