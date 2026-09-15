import factory

from users.models import CustomUser


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = CustomUser
        skip_postgeneration_save = True

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.Sequence(lambda n: f"user{n}")
    first_name = "Test"
    last_name = "User"
    role = CustomUser.Role.ADMIN

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted or "Password123!"
        self.set_password(password)

        if create:
            self.save()