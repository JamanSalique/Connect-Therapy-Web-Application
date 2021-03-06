from datetime import date
from urllib.parse import urlencode

from django.test import TestCase, RequestFactory
from django.urls import reverse_lazy

from connect_therapy.models import *
from connect_therapy.views.patient import ViewBookableAppointmentsView


class AppointmentBookingViewTest(TestCase):

    def setUp(self):
        # Create two users
        test_user_1 = User.objects.create_user(username='testuser1')
        test_user_1.set_password('12345')
        test_user_1.save()

        self.test_pat_1 = Patient(user=test_user_1,
                                  email_confirmed=True,
                                  gender='M',
                                  mobile="+447476666555",
                                  date_of_birth=date(year=1995, month=1, day=1))
        self.test_pat_1.save()

        test_user_2 = User.objects.create_user(username='testuser2')
        test_user_2.set_password('12345')
        test_user_2.save()

        self.test_pat_2 = Patient(user=test_user_2,
                                  email_confirmed=True,
                                  gender='M',
                                  mobile="+447476666555",
                                  date_of_birth=date(year=1995, month=1, day=1))
        self.test_pat_2.save()

        self.test_user_3 = User.objects.create_user(username='testuser3')
        self.test_user_3.set_password('12345')

        self.test_user_3.save()

        self.test_prac_1 = Practitioner(user=self.test_user_3,
                                        email_confirmed=True,
                                        address_line_1="My home",
                                        postcode="EC12 1CV",
                                        mobile="+447577293232",
                                        bio="Hello")
        self.test_prac_1.save()

        self.test_user_4 = User.objects.create_user(username='testuser4')
        self.test_user_4.set_password('12345')

        self.test_user_4.save()

        self.test_prac_2 = Practitioner(user=self.test_user_4,
                                        email_confirmed=True,
                                        address_line_1="My home",
                                        postcode="EC12 1CV",
                                        mobile="+447577293232",
                                        bio="Hello")
        self.test_prac_2.save()

        self.test_user_5 = User.objects.create_user(username='testuser5')
        self.test_user_5.set_password('12345')

        self.test_user_5.save()

        self.test_prac_3 = Practitioner(user=self.test_user_5,
                                        email_confirmed=True,
                                        address_line_1="My home",
                                        postcode="EC12 1CV",
                                        mobile="+447577293232",
                                        bio="Hello")
        self.test_prac_3.save()

        self.test_appointment_1 = Appointment(
            practitioner=self.test_prac_1,
            start_date_and_time=datetime(year=2019,
                                         month=4,
                                         day=2,
                                         hour=15,
                                         minute=16),
            length=timedelta(hours=1)
        )
        self.test_appointment_1.save()

        self.test_appointment_2 = Appointment(
            practitioner=self.test_prac_1,
            start_date_and_time=datetime(year=2019,
                                         month=4,
                                         day=2,
                                         hour=15,
                                         minute=16),
            length=timedelta(hours=1)
        )
        self.test_appointment_2.save()

        self.test_appointment_3 = Appointment(
            practitioner=self.test_prac_1,
            start_date_and_time=datetime(year=2019,
                                         month=4,
                                         day=2,
                                         hour=15,
                                         minute=16),
            length=timedelta(hours=1)
        )
        self.test_appointment_3.save()

        self.test_appointment_4 = Appointment(
            practitioner=self.test_prac_1,
            start_date_and_time=datetime(year=2019,
                                         month=4,
                                         day=2,
                                         hour=16,
                                         minute=16),
            length=timedelta(hours=1)
        )
        self.test_appointment_4.save()

        self.test_appointment_5 = Appointment(
            practitioner=self.test_prac_1,
            start_date_and_time=datetime(year=2019,
                                         month=4,
                                         day=2,
                                         hour=17,
                                         minute=16),
            length=timedelta(hours=1)
        )
        self.test_appointment_5.save()

        self.test_appointment_6 = Appointment(
            practitioner=self.test_prac_1,
            start_date_and_time=datetime(year=2019,
                                         month=4,
                                         day=2,
                                         hour=18,
                                         minute=16),
            length=timedelta(hours=1)
        )
        self.test_appointment_6.save()

        self.test_appointment_7 = Appointment(
            practitioner=self.test_prac_1,
            start_date_and_time=timezone.now() + timedelta(days=28),
            length=timedelta(hours=1)
        )
        self.test_appointment_7.save()

        self.test_appointment_8 = Appointment(
            practitioner=self.test_prac_2,
            start_date_and_time=timezone.now() + timedelta(days=28),
            length=timedelta(hours=1)
        )
        self.test_appointment_8.save()

        self.test_appointment_9 = Appointment(
            practitioner=self.test_prac_2,
            start_date_and_time=timezone.now() - timedelta(days=28),
            length=timedelta(hours=1)
        )
        self.test_appointment_9.save()

    def test_redirect_if_not_logged_in_init_booking_page(self):
        resp = self.client.get(reverse_lazy('connect_therapy:patient-book-appointment', kwargs={'pk': 1}))
        self.assertRedirects(resp, '/patient/login?next=/patient/book-appointment/1')

    def test_logged_in_user_correct_template_init_booking_page(self):
        login = self.client.login(username="testuser1", password="12345")
        resp = self.client.get(reverse_lazy('connect_therapy:patient-book-appointment', kwargs={'pk': 1}))

        # Check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(resp, 'connect_therapy/patient/bookings/view-available.html')

    def test_redirect_if_not_logged_in_review_booking_page(self):
        resp = self.client.get(reverse_lazy('connect_therapy:patient-book-appointment-review', kwargs={'pk': 1}))
        self.assertRedirects(resp, '/patient/login?next=/patient/book-appointment/1/review')

    def test_logged_in_user_correct_template_review_booking_page(self):
        login = self.client.login(username="testuser1", password="12345")
        resp = self.client.get(reverse_lazy('connect_therapy:patient-book-appointment-review', kwargs={'pk': 1}))

        # Check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(resp, 'connect_therapy/patient/bookings/review-selection.html')

    def test_redirect_if_not_logged_in_checkout(self):
        resp = self.client.get(reverse_lazy('connect_therapy:patient-checkout'))
        self.assertRedirects(resp, '/patient/login?next=/patient/checkout')

    def test_logged_in_user_correct_template_checkout(self):
        login = self.client.login(username="testuser1", password="12345")
        resp = self.client.get(reverse_lazy('connect_therapy:patient-checkout'))

        # Check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(resp, 'connect_therapy/patient/bookings/checkout.html')

    def test_redirect_if_practitioner_init_booking_page(self):
        login = self.client.login(username="testuser3", password="12345")
        resp = self.client.get(reverse_lazy('connect_therapy:patient-book-appointment', kwargs={'pk': 1}))

        self.assertRedirects(resp, '/patient/login?next=/patient/book-appointment/1')

    def test_redirect_if_practitioner_review_booking_page(self):
        login = self.client.login(username="testuser3", password="12345")
        resp = self.client.get(reverse_lazy('connect_therapy:patient-book-appointment-review', kwargs={'pk': 1}))

        self.assertRedirects(resp, '/patient/login?next=/patient/book-appointment/1/review')

    def test_redirect_if_practitioner_visits_checkout_page(self):
        login = self.client.login(username="testuser3", password="12345")
        resp = self.client.get(reverse_lazy('connect_therapy:patient-checkout'))

        self.assertRedirects(resp, '/patient/login?next=/patient/checkout')

    def test_correct_page_if_user_visits_list_practitioner_page(self):
        login = self.client.login(username="testuser1", password="12345")
        resp = self.client.get(reverse_lazy('connect_therapy:patient-view-practitioners'))

        # Check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(resp, 'connect_therapy/patient/bookings/list-practitioners.html')

    def test_redirect_if_anonymous_visits_list_practitioner_page(self):
        resp = self.client.get(reverse_lazy('connect_therapy:patient-view-practitioners'))
        self.assertRedirects(resp, '/patient/login?next=/patient/view-practitioners')

    def test_redirect_if_practitioner_visits_list_practitioner_page(self):
        login = self.client.login(username="testuser3", password="12345")
        resp = self.client.get(reverse_lazy('connect_therapy:patient-view-practitioners'))
        self.assertRedirects(resp, '/patient/login?next=/patient/view-practitioners')

    def test_view_bookable_appointments_page_post_valid_form(self):
        # this tests what happens when we submit some data to the view page using the post method
        login = self.client.login(username="testuser1", password="12345")
        resp_get = self.client.get(reverse_lazy('connect_therapy:patient-book-appointment', kwargs={'pk': 1}))

        self.assertEquals(resp_get.status_code, 200)
        # only one test has been done as the user input is limited to entering only what we want.
        # so the user cannot submit erroneous data

        data = urlencode({
            'date': datetime.now().date()
        })
        resp_post = self.client.post(reverse_lazy('connect_therapy:patient-book-appointment', kwargs={'pk': 1}), data,
                                     content_type="application/x-www-form-urlencoded")

        self.assertEquals(resp_post.status_code, 200)

    def test_view_bookable_appointments_page_post_invalid_form_as_date_in_past(self):
        # this tests what happens when we submit some data to the view page using the post method
        login = self.client.login(username="testuser1", password="12345")
        resp_get = self.client.get(reverse_lazy('connect_therapy:patient-book-appointment', kwargs={'pk': 1}))

        self.assertEquals(resp_get.status_code, 200)
        # only one test has been done as the user input is limited to entering only what we want.
        # so the user cannot submit erroneous data

        data = urlencode({
            'date': datetime.now().date() - timedelta(days=10)
        })
        resp_post = self.client.post(reverse_lazy('connect_therapy:patient-book-appointment', kwargs={'pk': 1}), data,
                                     content_type="application/x-www-form-urlencoded")

        self.assertEquals(resp_post.status_code, 200)

    def test_review_bookable_appointments_page_post_with_valid_appointments(self):
        # this tests what happens when we submit some data to the review page by post method
        login = self.client.login(username="testuser1", password="12345")
        resp_get = self.client.get(reverse_lazy('connect_therapy:patient-book-appointment-review', kwargs={'pk': 1}))

        self.assertEquals(resp_get.status_code, 200)

        # the app_is's below belong to valid appointments defined in the setUp(...) method
        resp_post = self.client.post(reverse_lazy('connect_therapy:patient-book-appointment-review', kwargs={'pk': 1}),
                                     {
                                         'app_id': [4, 5, 6]
                                     })

        # check that the appointments have been added to the basket
        apps = self.client.session['bookable_appointments']
        apps_list = Appointment.convert_dictionaries_to_appointments(apps)
        self.assertEquals(len(apps_list), 1)  # 1 appointment as 3 appointments would be merged

        self.assertEquals(resp_post.status_code, 200)

    def test_review_bookable_appointments_page_post_with_overlapping_appointments(self):
        login = self.client.login(username="testuser1", password="12345")
        resp_get = self.client.get(reverse_lazy('connect_therapy:patient-book-appointment-review', kwargs={'pk': 1}))

        self.assertEquals(resp_get.status_code, 200)
        resp_post = self.client.post(reverse_lazy('connect_therapy:patient-book-appointment-review', kwargs={'pk': 1}),
                                     {
                                         'app_id': [1, 2, 3]
                                     })

        # the basket should not have been created as no appointments should be added to it
        try:
            self.client.session['bookable_appointments']
            self.assertTrue(False)
        except KeyError:
            self.assertTrue(True)
        self.assertEquals(resp_post.status_code, 200)

    def test_review_bookable_appointments_page_post_with_invalid_appointments(self):
        login = self.client.login(username="testuser1", password="12345")
        resp_get = self.client.get(reverse_lazy('connect_therapy:patient-book-appointment-review', kwargs={'pk': 1}))

        self.assertEquals(resp_get.status_code, 200)
        resp_post = self.client.post(reverse_lazy('connect_therapy:patient-book-appointment-review', kwargs={'pk': 1}),
                                     {
                                         'app_id': [12, 13, 14]
                                     })

        # the basket should not have been created as no appointments should be added to it
        try:
            self.client.session['bookable_appointments']
            self.assertTrue(False)
        except KeyError:
            self.assertTrue(True)

        self.assertEquals(resp_post.status_code, 200)

    def test_review_bookable_appointments_page_post_with_no_appointments(self):
        login = self.client.login(username="testuser1", password="12345")
        resp_get = self.client.get(reverse_lazy('connect_therapy:patient-book-appointment-review', kwargs={'pk': 1}))

        self.assertEquals(resp_get.status_code, 200)
        resp_post = self.client.post(reverse_lazy('connect_therapy:patient-book-appointment-review', kwargs={'pk': 1}),
                                     {
                                         'app_id': []
                                     })

        # the basket should not have been created as no appointments should be added to it
        try:
            self.client.session['bookable_appointments']
            self.assertTrue(False)
        except KeyError:  # KeyError means we cant find the basket key
            self.assertTrue(True)

        self.assertEquals(resp_post.status_code, 302)
        self.assertRedirects(resp_post, reverse_lazy("connect_therapy:patient-book-appointment", kwargs={'pk': 1}))

    def test_checkout_page_booking_mergeable_appointments(self):
        # some repetition to start with as we need to add some stuff to our checkout and I want this test to work
        # in isolation to all other tests - as it should - i think...

        login = self.client.login(username="testuser1", password="12345")
        resp_get_review = self.client.get(
            reverse_lazy('connect_therapy:patient-book-appointment-review', kwargs={'pk': 1}))

        self.assertEquals(resp_get_review.status_code, 200)

        # the app_is's below belong to valid appointments defined in the setUp(...) method
        resp_post_review = self.client.post(
            reverse_lazy('connect_therapy:patient-book-appointment-review', kwargs={'pk': 1}),
            {
                'app_id': [4, 5, 6]
            })

        # check that the appointments have been added to the basket
        apps = self.client.session['bookable_appointments']
        apps_list = Appointment.convert_dictionaries_to_appointments(apps)
        self.assertEquals(len(apps_list), 1)  # 1 appointment as 3 appointments above would be merged into 1

        # check that the appointments are unbooked
        for app in apps_list:
            self.assertEquals(app.patient, None)

        self.assertEquals(resp_post_review.status_code, 200)

        resp_get_checkout = self.client.get(reverse_lazy('connect_therapy:patient-checkout'))

        self.assertEquals(resp_get_checkout.status_code, 200)
        self.assertTemplateUsed("connect_therapy/patient/booking/checkout.html")

        # checkout - book appointments with post request below
        resp_get_checkout = self.client.post(reverse_lazy("connect_therapy:patient-checkout"), {
            "checkout": "checkout"
        })

        # the basket (and contents) should have been deleted
        try:
            self.client.session['bookable_appointments']
            self.assertTrue(False)
        except KeyError:  # KeyError means we cant find the basket key
            self.assertTrue(True)

        # the mergeable appointments should have been deleted from session storage
        try:
            self.client.session['merged_appointments']
            self.assertTrue(False)
        except KeyError:  # KeyError means we cant find the basket key
            self.assertTrue(True)

        # finally check that the appointment we booked has indeed been booked.
        # only one appointment should belong to the user with username "testuser1"
        appointments = Appointment.objects.all().filter(patient__user__username="testuser1")
        self.assertEquals(len(appointments), 1)

    def test_checkout_page_booking_no_appointments(self):
        # some repetition to start with as we need to add some stuff to our checkout and I want this test to work
        # in isolation to all other tests - as it should - i think...

        login = self.client.login(username="testuser1", password="12345")
        self.client.session['bookable_appointments'] = None

        # checkout - book appointments with post request below
        resp_get_checkout = self.client.post(reverse_lazy("connect_therapy:patient-checkout"), {
            "checkout": "checkout"
        })
        self.assertEquals(resp_get_checkout.status_code, 200)

    def test_checkout_page_booking_booked_appointment(self):
        # some repetition to start with as we need to add some stuff to our checkout and I want this test to work
        # in isolation to all other tests - as it should - i think...

        login = self.client.login(username="testuser1", password="12345")
        resp_get_review = self.client.get(
            reverse_lazy('connect_therapy:patient-book-appointment-review', kwargs={'pk': 1}))

        self.assertEquals(resp_get_review.status_code, 200)

        # the app_is's below belong to valid appointments defined in the setUp(...) method
        resp_post_review = self.client.post(
            reverse_lazy('connect_therapy:patient-book-appointment-review', kwargs={'pk': 1}),
            {
                'app_id': [7]
            })

        # check that the appointments have been added to the basket
        apps = self.client.session['bookable_appointments']
        apps_list = Appointment.convert_dictionaries_to_appointments(apps)
        self.assertEquals(len(apps_list), 1)  # 1 appointment should be in the basket

        # check that the appointments are unbooked
        for app in apps_list:
            self.assertEquals(app.patient, None)

        self.assertEquals(resp_post_review.status_code, 200)

        resp_get_checkout = self.client.get(reverse_lazy('connect_therapy:patient-checkout'))

        self.assertEquals(resp_get_checkout.status_code, 200)
        self.assertTemplateUsed("connect_therapy/patient/booking/checkout.html")
        app = Appointment.objects.get(pk=7)
        app.patient = self.test_pat_2
        app.save()

        # checkout - book appointments with post request below
        resp_post_checkout = self.client.post(reverse_lazy("connect_therapy:patient-checkout"), {
            "checkout": "checkout"
        })

        # the basket (and contents) should have been deleted
        try:
            self.client.session['bookable_appointments']
            self.assertTrue(False)
        except KeyError:  # KeyError means we cant find the basket key
            self.assertTrue(True)

        # finally check that the appointment we booked has indeed been booked.
        # only one appointment should belong to the user with username "testuser1"
        appointments = Appointment.objects.all().filter(patient__user__username="testuser1")
        self.assertEquals(len(appointments), 0)

    def test_checkout_page_booking_unmergeable_appointments(self):
        # some repetition to start with as we need to add some stuff to our checkout and I want this test to work
        # in isolation to all other tests - as it should - i think...

        login = self.client.login(username="testuser1", password="12345")
        resp_get_review = self.client.get(
            reverse_lazy('connect_therapy:patient-book-appointment-review', kwargs={'pk': 1}))

        self.assertEquals(resp_get_review.status_code, 200)

        # the app_is's below belong to valid appointments defined in the setUp(...) method
        resp_post_review = self.client.post(
            reverse_lazy('connect_therapy:patient-book-appointment-review', kwargs={'pk': 1}),
            {
                'app_id': [4]
            })

        # check that the appointments have been added to the basket
        apps = self.client.session['bookable_appointments']
        apps_list = Appointment.convert_dictionaries_to_appointments(apps)
        self.assertEquals(len(apps_list), 1)  # 1 appointment should be in the basket

        # check that the appointments are unbooked
        for app in apps_list:
            self.assertEquals(app.patient, None)

        self.assertEquals(resp_post_review.status_code, 200)

        resp_get_checkout = self.client.get(reverse_lazy('connect_therapy:patient-checkout'))

        self.assertEquals(resp_get_checkout.status_code, 200)
        self.assertTemplateUsed("connect_therapy/patient/booking/checkout.html")

        # checkout - book appointments with post request below
        resp_post_checkout = self.client.post(reverse_lazy("connect_therapy:patient-checkout"), {
            "checkout": "checkout"
        })

        # the basket (and contents) should have been deleted
        try:
            self.client.session['bookable_appointments']
            self.assertTrue(False)
        except KeyError:  # KeyError means we cant find the basket key
            self.assertTrue(True)

        # finally check that the appointment we booked has indeed been booked.
        # only one appointment should belong to the user with username "testuser1"
        appointments = Appointment.objects.all().filter(patient__user__username="testuser1")
        self.assertEquals(len(appointments), 1)

    def test_checkout_delete(self):
        login = self.client.login(username="testuser1", password="12345")
        resp_get_review = self.client.get(
            reverse_lazy('connect_therapy:patient-book-appointment-review', kwargs={'pk': 1}))

        self.assertEquals(resp_get_review.status_code, 200)

        # the app_is's below belong to valid appointments defined in the setUp(...) method
        resp_post_review = self.client.post(
            reverse_lazy('connect_therapy:patient-book-appointment-review', kwargs={'pk': 1}),
            {
                'app_id': [4, 6]
            })

        # check that the appointments have been added to the basket
        apps = self.client.session['bookable_appointments']
        apps_list = Appointment.convert_dictionaries_to_appointments(apps)
        self.assertEquals(len(apps_list), 2)  # 2 appointment should be in the basket

        # check that the appointments are unbooked
        for app in apps_list:
            self.assertEquals(app.patient, None)

        self.assertEquals(resp_post_review.status_code, 200)

        resp_get_checkout = self.client.get(reverse_lazy('connect_therapy:patient-checkout'))

        self.assertEquals(resp_get_checkout.status_code, 200)
        self.assertTemplateUsed("connect_therapy/patient/booking/checkout.html")

        resp_post_checkout_delete = self.client.post(reverse_lazy("connect_therapy:patient-checkout"), {
            "delete": apps_list[0].session_id
        })

        # check that the appointments have been added to the basket
        apps = self.client.session['bookable_appointments']
        apps_list = Appointment.convert_dictionaries_to_appointments(apps)
        self.assertEquals(len(apps_list), 1)  # 1 appointment should be in the basket

    def test_checkout_delete_invalid_session_id(self):
        login = self.client.login(username="testuser1", password="12345")
        resp_get_review = self.client.get(
            reverse_lazy('connect_therapy:patient-book-appointment-review', kwargs={'pk': 1}))

        self.assertEquals(resp_get_review.status_code, 200)

        # the app_is's below belong to valid appointments defined in the setUp(...) method
        resp_post_review = self.client.post(
            reverse_lazy('connect_therapy:patient-book-appointment-review', kwargs={'pk': 1}),
            {
                'app_id': [4, 6]
            })

        # check that the appointments have been added to the basket
        apps = self.client.session['bookable_appointments']
        apps_list = Appointment.convert_dictionaries_to_appointments(apps)
        self.assertEquals(len(apps_list), 2)  # 2 appointment should be in the basket

        # check that the appointments are unbooked
        for app in apps_list:
            self.assertEquals(app.patient, None)

        self.assertEquals(resp_post_review.status_code, 200)

        resp_get_checkout = self.client.get(reverse_lazy('connect_therapy:patient-checkout'))

        self.assertEquals(resp_get_checkout.status_code, 200)
        self.assertTemplateUsed("connect_therapy/patient/booking/checkout.html")

        resp_post_checkout_delete = self.client.post(reverse_lazy("connect_therapy:patient-checkout"), {
            "delete": "fake-session-id"
        })

        # check that the appointments have been added to the basket
        apps = self.client.session['bookable_appointments']
        apps_list = Appointment.convert_dictionaries_to_appointments(apps)
        self.assertEquals(len(apps_list), 2)  # 2 appointment should be in the basket nothing should be deleted

    def test_view_bookable_when_form_invalid(self):
        test_user_2 = User.objects.create_user(username='testuser3943')
        test_user_2.set_password('12345')

        test_user_2.save()

        test_prac_1 = Practitioner(user=test_user_2,
                                   address_line_1="My home",
                                   postcode="EC12 1CV",
                                   mobile="+447577293232",
                                   bio="Hello",
                                   is_approved=True,
                                   email_confirmed=True)
        test_prac_1.save()

        factory = RequestFactory()
        request = factory.post('patient/book-appointment/{}'.format(test_prac_1.pk))
        request.POST = {}
        view = ViewBookableAppointmentsView()
        view.request = request
        view.get_object = lambda queryset=None: test_prac_1
        response = view.post(request, 1)
        self.assertEqual(response.status_code, 200)

    def test_practitioner_overlap_overlapping_overlaps(self):
        # should overlap
        overlap_bool, overlaps = Appointment.get_appointment__practitioner_overlaps(self.test_appointment_1,
                                                                                    self.test_prac_1)
        self.assertFalse(overlap_bool)

    def test_practitioner_overlap_overlapping_no_overlaps(self):
        # should not overlap overlap
        overlap_bool, overlaps = Appointment.get_appointment__practitioner_overlaps(self.test_appointment_1,
                                                                                    self.test_prac_2)
        self.assertTrue(overlap_bool)


    def test_practitioner_overlap_overlapping_new_practitioner(self):
        # should not overlap overlap
        overlap_bool, overlaps = Appointment.get_appointment__practitioner_overlaps(self.test_appointment_1,
                                                                                    self.test_prac_3)
        self.assertTrue(overlap_bool)

    def test_validity_method_with_past_appointments(self):
        self.assertFalse(Appointment.check_validity([9],self.test_prac_2.id))