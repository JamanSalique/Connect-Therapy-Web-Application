from django.test import TestCase

from connect_therapy.forms.practitioner.custom_duration_field import compress_duration, decompress_duration
from connect_therapy.forms.practitioner.practitioner import *
from connect_therapy.models import Practitioner


class PractitionerSignUpFormTests(TestCase):
    def test_when_already_exists(self):
        user = User(username="test@example.com", password="woofwoof12")
        user.save()
        form = PractitionerSignUpForm(data={
            'first_name': 'Dave',
            'last_name': 'Daverson',
            'address_line_1': 'M',
            'postcode': 'XXXXX',
            'mobile': '+447075593323',
            'email': 'test@example.com',
            'bio': 'ABC',
            'password1': 'meowmeow1',
            'password2': 'meowmeow1'
        })
        self.assertFalse(form.is_valid())

    def test_when_password_does_not_match(self):
        form = PractitionerSignUpForm(data={
            'first_name': 'Dave',
            'last_name': 'Daverson',
            'address_line_1': 'M',
            'postcode': 'XXXXX',
            'mobile': '+447075593323',
            'email': 'test@example.com',
            'bio': 'ABC',
            'password1': 'meowmeow1',
            'password2': 'meowmeow2'
        })
        self.assertFalse(form.is_valid())

    def test_when_email_is_not_valid(self):
        form = PractitionerSignUpForm(data={
            'first_name': 'Dave',
            'last_name': 'Daverson',
            'address_line_1': 'M',
            'postcode': 'XXXXX',
            'mobile': '+447075593323',
            'email': 'testexample.com',
            'bio': 'ABC',
            'password1': 'meowmeow1',
            'password2': 'meowmeow1'
        })
        self.assertFalse(form.is_valid())

    def test_when_mobile_is_too_long(self):
        form = PractitionerSignUpForm(data={
            'first_name': 'Dave',
            'last_name': 'Daverson',
            'address_line_1': 'M',
            'postcode': 'XXXXX',
            'mobile': '+447075593328282838983233',
            'email': 'test@example.com',
            'bio': 'ABC',
            'password1': 'meowmeow1',
            'password2': 'meowmeow1'
        })
        self.assertFalse(form.is_valid())

    def test_when_valid(self):
        form = PractitionerSignUpForm(data={
            'first_name': 'Dave',
            'last_name': 'Daverson',
            'address_line_1': 'M',
            'postcode': 'XXXXX',
            'mobile': '+447075593323',
            'email': 'test@example.com',
            'bio': 'ABC',
            'password1': 'meowmeow1',
            'password2': 'meowmeow1'
        })
        self.assertTrue(form.is_valid())


class PractitionerLoginFormTests(TestCase):
    def test_when_practitioner_exists_and_valid(self):
        user = User.objects.create_user(username='test@example.com',
                                        password='woofwoof12'
                                        )
        practitioner = Practitioner(user=user,
                                    mobile="+44848482732",
                                    email_confirmed=True,
                                    bio="ABC",
                                    address_line_1="XXX",
                                    address_line_2="XXXXX",
                                    is_approved=True
                                    )
        practitioner.save()
        form = PractitionerLoginForm(data={
            'username': 'test@example.com',
            'password': 'woofwoof12'
        })
        self.assertTrue(form.is_valid())

    def test_when_practitioner_exists_and_valid_but_not_approved(self):
        user = User.objects.create_user(username='test@example.com',
                                        password='woofwoof12'
                                        )
        practitioner = Practitioner(user=user,
                                    mobile="+44848482732",
                                    bio="ABC",
                                    address_line_1="XXX",
                                    address_line_2="XXXXX",
                                    is_approved=False
                                    )
        practitioner.save()
        form = PractitionerLoginForm(data={
            'username': 'test@example.com',
            'password': 'woofwoof12'
        })
        self.assertFalse(form.is_valid())

    def test_when_practitioner_does_not_exist(self):
        user = User.objects.create_user(username='test@example.com',
                                        password='woofwoof12'
                                        )
        form = PractitionerLoginForm(data={
            'username': 'test@example.com',
            'password': 'woofwoof12'
        })
        self.assertFalse(form.is_valid())

    def test_when_password_invalid(self):
        user = User.objects.create_user(username='test@example.com',
                                        password='woofwoof12'
                                        )
        practitioner = Practitioner(user=user,
                                    mobile="+44848482732",
                                    bio="ABC",
                                    address_line_1="XXX",
                                    address_line_2="XXXXX",
                                    is_approved=True
                                    )
        practitioner.save()
        form = PractitionerLoginForm(data={
            'username': 'test@example.com',
            'password': 'woofwoof11'
        })
        self.assertFalse(form.is_valid())

    def test_when_username_invalid(self):
        user = User.objects.create_user(username='test@example.com',
                                        password='woofwoof12'
                                        )
        practitioner = Practitioner(user=user,
                                    mobile="+44848482732",
                                    bio="ABC",
                                    address_line_1="XXX",
                                    address_line_2="XXXXX",
                                    is_approved=True
                                    )
        practitioner.save()
        form = PractitionerLoginForm(data={
            'username': 'test@demo.com',
            'password': 'woofwoof12'
        })
        self.assertFalse(form.is_valid())


class PractitionerEditProfileTests(TestCase):
    # Test that a patient can successfully update their mobile.
    def test_edit_fields(self):
        user = User.objects.create_user(username='test@example.com',
                                        password='testpassword',
                                        first_name='John',
                                        last_name='Smith'
                                        )
        practitioner = Practitioner(user=user,
                                    address_line_1='19 Langham Gardens',
                                    address_line_2='Ealing',
                                    postcode='W13 8PZ',
                                    mobile='+447476565333',
                                    bio='text'
                                    )
        practitioner.save()
        practitioner = PractitionerForm(instance=user.practitioner, data={
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'test1@example.com',
            'mobile': '+447075593323',
            'address_line_1': '39 buckingham Avenue',
            'address_line_2': 'Ealing',
            'postcode': 'UB6 7RD',
            'bio': 'more text'
        })
        practitioner.save()
        self.assertTrue(practitioner.is_valid())
        self.assertEqual(str(user.practitioner.mobile), '+447075593323')
        self.assertEqual(str(user.practitioner.address_line_1), '39 buckingham Avenue')
        self.assertEqual(str(user.practitioner.postcode), 'UB6 7RD')
        self.assertEqual(str(user.practitioner.bio), 'more text')

    # Test that a practitioner can successfully update their email.
    def test_edit_email(self):
        user = User.objects.create_user(username='test@example.com',
                                        password='testpassword',
                                        first_name='John',
                                        last_name='Smith'
                                        )
        practitioner = Practitioner(user=user,
                                    address_line_1='19 Langham Gardens',
                                    address_line_2='ealing',
                                    postcode='W13 8PZ',
                                    mobile='+447476565333',
                                    bio='text',
                                    is_approved=True
                                    )
        practitioner.save()
        practitioner = PractitionerUserForm(instance=user, data={
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'test1@example.com',
        })
        practitioner.save()
        self.assertTrue(practitioner.is_valid())
        self.assertEqual(str(user.email), 'test1@example.com')

    def test_valid_set_appointment_form(self):
        form = PractitionerDefineAppointmentForm(data={
            'start_date_and_time': datetime.datetime.now(),
            'length_0': 2,
            'length_1': 0
        })
        self.assertTrue(form.is_valid())

    def test_invalid_set_appointment_form_one(self):
        form = PractitionerDefineAppointmentForm(data={
            'start_date_and_time': datetime.datetime.now(),
            'length_0': 34535,
            'length_1': 3455
        })
        self.assertFalse(form.is_valid())

    def test_invalid_set_appointment_form_two(self):
        form = PractitionerDefineAppointmentForm(data={
            'start_date_and_time': datetime.datetime.now(),
            'length_0': "aa",
            'length_1': "bb"
        })
        self.assertFalse(form.is_valid())

    def test_invalid_set_appointment_form_one(self):
        form = PractitionerDefineAppointmentForm(data={
            'start_date_and_time': datetime.datetime.now(),
        })
        self.assertTrue(form.is_valid())

    def test_custom_duration_field_compression_function(self):
        data = [2, 0]
        self.assertEquals(compress_duration(data), "2h0m")

        data = [2, 30]
        self.assertEquals(compress_duration(data), "2h30m")

        data = [2323, 32132]
        self.assertEquals(compress_duration(data), "2323h32132m")

        data = []
        self.assertEquals(compress_duration(data), "")

    def test_custom_duration_field_decompression_function(self):
        data = "2h0m"
        self.assertEquals(decompress_duration(data), [2, 0])

        data = "2h30m"
        self.assertEquals(decompress_duration(data), [2, 30])

        data = "2323h32132m"
        self.assertEquals(decompress_duration(data), [2323, 32132])

        data = ""
        self.assertEquals(decompress_duration(data), [None, None])
