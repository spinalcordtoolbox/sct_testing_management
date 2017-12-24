from django.test import TestCase

# Create your tests here.
class TestSubject(TestCase):
    def setUp(self):
        self.subject = self.make_subject()
