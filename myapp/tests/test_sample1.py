from django.test import TransactionTestCase


class SampleTestCase(TransactionTestCase):

    def test1(self):
        self.assertTrue(True)
