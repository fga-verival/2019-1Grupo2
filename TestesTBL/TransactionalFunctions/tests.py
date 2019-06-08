import datetime

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


def test_property(property_name, object):

    try:

        return True, object.__getattribute__(property_name)

    except Exception as e:

        return False, e


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

    def test_counter_name(self):

        def generate_name_with_n_letters(n):
            return "a" * n

        self.assertEqual(test_field('counter_name', 0, generate_name_with_n_letters), False)
        self.assertEqual(test_field('counter_name', 3, generate_name_with_n_letters), False)
        self.assertEqual(test_field('counter_name', 50, generate_name_with_n_letters), True)
        self.assertEqual(test_field('counter_name', 100, generate_name_with_n_letters), True)

    def test_date(self):

        args = self.default_args.copy()
        del args['date']

        t = TransactionalFunction(**args)
        t.save()

        today = datetime.date.today()

        self.assertEquals(t.date, today)
        self.assertNotEqual(t.date, today + datetime.timedelta(days=1))
        self.assertNotEqual(t.date, today - datetime.timedelta(days=1))

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

    def test_low_complexity(self):

        t = TransactionalFunction(**self.default_args)

        t.functionality_type = 1 # type == EE
        t.ALR_aumount = None
        t.DER_aumount = 1
        self.assertEquals(test_property('transactional_complexity', t)[0], False)

        t.functionality_type = 2  # type == CE
        t.ALR_aumount = 0
        t.DER_aumount = -1
        self.assertEquals(test_property('transactional_complexity', t)[0], False)

        t.functionality_type = 3  # type == SE
        t.ALR_aumount = 0
        t.DER_aumount = 1
        self.assertEquals(test_property('transactional_complexity', t)[1], 'BAIXA')

        t.functionality_type = 1  # type == SE
        t.ALR_aumount = 1
        t.DER_aumount = 5
        self.assertEquals(test_property('transactional_complexity', t)[1], 'BAIXA')

    def test_medium_complexity(self):

        t = TransactionalFunction(**self.default_args)

        t.functionality_type = 3  # type == SE
        t.ALR_aumount = None
        t.DER_aumount = 1
        self.assertEquals(test_property('transactional_complexity', t)[0], False)

        t.functionality_type = 3  # type == SE
        t.ALR_aumount = 2
        t.DER_aumount = 15
        self.assertNotEqual(test_property('transactional_complexity', t)[0], 'MEDIA')

        t.functionality_type = 2  # type == CE
        t.ALR_aumount = 3
        t.DER_aumount = 19
        self.assertEquals(test_property('transactional_complexity', t)[1], 'MEDIA')

        t.functionality_type = 1  # type == EE
        t.ALR_aumount = 1
        t.DER_aumount = 15
        self.assertNotEqual(test_property('transactional_complexity', t)[1], 'MEDIA')

    def test_high_complexity(self):

        t = TransactionalFunction(**self.default_args)

        t.functionality_type = 2  # type == CE
        t.ALR_aumount = None
        t.DER_aumount = 1
        self.assertEquals(test_property('transactional_complexity', t)[0], False)

        t.functionality_type = 1  # type == EE
        t.ALR_aumount = 3
        t.DER_aumount = 4
        self.assertNotEqual(test_property('transactional_complexity', t)[0], 'ALTA')

        t.functionality_type = 2  # type == CE
        t.ALR_aumount = 3
        t.DER_aumount = 20
        self.assertEquals(test_property('transactional_complexity', t)[1], 'ALTA')

        t.functionality_type = 3  # type == SE
        t.ALR_aumount = 4
        t.DER_aumount = 3
        self.assertNotEqual(test_property('transactional_complexity', t)[1], 'ALTA')

    def test_functional_points_for_ee_and_ce(self):

        t = TransactionalFunction(**self.default_args)

        # low complexity
        t.ALR_aumount = 0
        t.DER_aumount = 1

        t.functionality_type = 1
        self.assertEquals(t.transactional_complexity, 'BAIXA')
        self.assertEquals(t.function_points_aumount, 3)

        t.functionality_type = 2
        self.assertEquals(t.transactional_complexity, 'BAIXA')
        self.assertEquals(t.function_points_aumount, 3)

        # medium complexity
        t.ALR_aumount = 2
        t.DER_aumount = 5

        t.functionality_type = 1
        self.assertEquals(t.transactional_complexity, 'MEDIA')
        self.assertEquals(t.function_points_aumount, 4)

        t.functionality_type = 2
        self.assertEquals(t.transactional_complexity, 'MEDIA')
        self.assertEquals(t.function_points_aumount, 4)

        # high complexity
        t.ALR_aumount = 4
        t.DER_aumount = 16

        t.functionality_type = 1
        self.assertEquals(t.transactional_complexity, 'ALTA')
        self.assertEquals(t.function_points_aumount, 6)

        t.functionality_type = 2
        self.assertEquals(t.transactional_complexity, 'ALTA')
        self.assertEquals(t.function_points_aumount, 6)

    def test_functional_points_for_se(self):

        t = TransactionalFunction(**self.default_args)

        # low complexity
        t.ALR_aumount = 0
        t.DER_aumount = 1

        t.functionality_type = 3

        self.assertEquals(t.transactional_complexity, 'BAIXA')
        self.assertEquals(t.function_points_aumount, 4)

        # medium complexity
        t.ALR_aumount = 2
        t.DER_aumount = 6

        self.assertEquals(t.transactional_complexity, 'MEDIA')
        self.assertEquals(t.function_points_aumount, 5)

        # high complexity
        t.ALR_aumount = 4
        t.DER_aumount = 20

        self.assertEquals(t.transactional_complexity, 'ALTA')
        self.assertEquals(t.function_points_aumount, 7)
