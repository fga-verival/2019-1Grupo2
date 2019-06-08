from django.test import TestCase

from .models import TransactionalFunction


class TestModel(TestCase):

    default_args = {
        'name': "name",
        'functionality_type': 1,
        'ALR_aumount': 2,
        'DER_aumount': 2,
        'counter_name': 'counter name',
        'date': '2000-01-01'
    }

    def setUp(self) -> None:
        pass

    def testName(self):

        def test_with_n_letters(n):
            try:

                args = self.default_args.copy()
                args['name'] = "a" * n

                t = TransactionalFunction(**args)
                t.save()

                return True

            except Exception as e:

                return False

        self.assertEqual(test_with_n_letters(0), False)
        self.assertEqual(test_with_n_letters(3), False)
        self.assertEqual(test_with_n_letters(50), True)
        self.assertEqual(test_with_n_letters(100), True)

