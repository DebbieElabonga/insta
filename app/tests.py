from django.test import TestCase

from .models import Profile, Post
from django.contrib.auth.models import User


class TestProfile(TestCase):
    def setUp(self):
        self.user = User(username='debbie')
        self.user.save()

        self.profile_test = Profile(id=1, name='image', profile_picture='a.jpg', bio='bio',
                                    user=self.user)




class TestPost(TestCase):
    def setUp(self):
        self.profile_test = Profile(name='salano', user=User(username='salano'))
        self.profile_test.save()

        self.image_test = Post(image='a.png', name='test', caption='default test', user=self.profile_test)


    def test_save_image(self):
        self.image_test.save_image()
        images = Post.objects.all()
        self.assertTrue(len(images) > 0)

    def test_delete_image(self):
        self.image_test.delete_image()
        after = Profile.objects.all()
        self.assertTrue(len(after) < 1)
