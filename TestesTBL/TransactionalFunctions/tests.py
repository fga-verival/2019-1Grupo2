from django.test import TestCase

from .models import TransactionalFunction


def test_field(field_name, value, generator=None):
    try:

        if generator is None:
            generator = lambda x: x

        args = TestModel.default_args.copy()
        args[field_name] = generator(value)

        t = TransactionalFunction(**args)
        t.save()

        return True

    except Exception as e:

        return False


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


    def test_name(self):

        def generate_name_with_n_letters(n):
            return "a" * n

        self.assertEqual(test_field('name', 0, generate_name_with_n_letters), False)
        self.assertEqual(test_field('name', 3, generate_name_with_n_letters), False)
        self.assertEqual(test_field('name', 50, generate_name_with_n_letters), True)
        self.assertEqual(test_field('name', 100, generate_name_with_n_letters), True)

    def test_functionality_type(self):

        def generate_value_from_display(display):

            choice_value = -1

            for index, choice in enumerate(TransactionalFunction.FUNCTIONALITY_TYPE_CHOICES):
                if choice[1] == display:
                    choice_value = choice[0]
                    break

            if choice_value == -1:
                return display
            else:
                return choice_value

        self.assertEqual(test_field('functionality_type', '', generate_value_from_display), False)
        self.assertEqual(test_field('functionality_type', 'TESTE', generate_value_from_display), False)
        self.assertEqual(test_field('functionality_type', 'caso', generate_value_from_display), False)
        self.assertEqual(test_field('functionality_type', 'EE', generate_value_from_display), True)
        self.assertEqual(test_field('functionality_type', 'CE', generate_value_from_display), True)
        self.assertEqual(test_field('functionality_type', 'SE', generate_value_from_display), True)

    def test_ALR_aumount(self):

        self.assertEqual(test_field('ALR_aumount', None), False)
        self.assertEqual(test_field('ALR_aumount', -2), False)
        self.assertEqual(test_field('ALR_aumount', -1), False)
        self.assertEqual(test_field('ALR_aumount', 0), True)
        self.assertEqual(test_field('ALR_aumount', 1), True)


    def test_DER_aumount(self):

        self.assertEqual(test_field('DER_aumount', None), False)
        self.assertEqual(test_field('DER_aumount', -2), False)
        self.assertEqual(test_field('DER_aumount', -1), False)
        self.assertEqual(test_field('DER_aumount', 0), False)
        self.assertEqual(test_field('DER_aumount', 1), True)
