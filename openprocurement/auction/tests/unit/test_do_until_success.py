from openprocurement.auction.utils import do_until_success

from mock import MagicMock, call


def get_until_success(number_of_attempts):

    class UntilSuccess(object):
        count = 0
        return_func = MagicMock(return_value=2)

        def __call__(self, *args, **kwargs):
            for i in range(number_of_attempts):
                self.count += 1
                if self.count < number_of_attempts:
                    raise Exception
                return self.return_func(*args, **kwargs)

    res = UntilSuccess()
    return res


class TestDoUntilSuccess(object):

    def test_do_until_success(self):
        func = MagicMock(return_value=4)
        number_of_attempts = 3
        args = (1, 2, 3)
        kwargs = {'1': 1, '2': 2}
        do_until_success(func, args, kwargs)
        func.assert_called_with(*args, **kwargs)
        res = get_until_success(number_of_attempts)
        do_until_success(res, args, kwargs, repeat=3)
        res.return_func.assert_called_with(*args, **kwargs)
