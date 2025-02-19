from django.contrib.auth.mixins import UserPassesTestMixin


class IsStaffRequiredMixin(UserPassesTestMixin):
    '''разреешить дейстия если пользователь is_staff'''
    def test_func(self):
        return self.request.user.is_staff
