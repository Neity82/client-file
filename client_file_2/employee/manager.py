from django.contrib.auth.base_user import BaseUserManager


class EmployeeManager(BaseUserManager):
    def create_user(self, username, office, password=None):
        user = self.model(
            username=self.get_by_natural_key(username),
            office=office,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, office, password):
        user = self.create_user(
            username,
            password=password,
            office=office,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
