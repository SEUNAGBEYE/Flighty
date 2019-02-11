import factory
import random
from factory.django import DjangoModelFactory
from user.models import User, UserProfile

class UserFactory(DjangoModelFactory):

    email = factory.Sequence(lambda n: 'person{0}@test.com'.format(n))
    password = factory.PostGeneration(lambda user, create, extracted: user.set_password(extracted))
    
    class Meta:
        model = User

class ProfileFactory(DjangoModelFactory):

    class Meta:
        model = UserProfile