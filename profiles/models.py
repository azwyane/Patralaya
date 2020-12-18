# django model fields
from django.db import models

# factory settings
from django.conf import settings

# User model from django auth app
from django.contrib.auth.models import User

# timezone
from django.utils import timezone

# reverse the parent content
from django.urls import reverse

#PIL
from PIL import Image

class Profile(models.Model):
    '''
    Profile specifies the Profile table in the database.
    Here the attributes are:
    - user: foreign key to User model defined in the admin app
    - profile_picture: image of the profile

    It refers to the social profile of the user. These fields are
    extensible for future.
    '''
    WORKING_STATUS_CHOICES= [
    ('student', 'Student'),
    ('teacher', 'Teacher'),
    ('none', 'Prefer no to say'),
    ]

    INTERESTED_FIELDS_CHOICES =[
        ('science','Science'),
        ('maths','Maths'),
        ('computer','Computer'),
        ('history','History'),
        ('health','Health'),
    ]


    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        primary_key=True
        )
    profile_picture = models.ImageField(
        upload_to='profile_picture',
        blank=True,
        null= True
        )
    following = models.ManyToManyField(
        'self',
        through='Follow',
        related_name='followers',
        symmetrical=False
        )
    bio = models.TextField(blank = True, null = True)
    current_status = models.CharField(
        max_length=10,
        choices = WORKING_STATUS_CHOICES,
        blank = True, null = True
        )
    interested_fields = models.CharField(
        max_length=10,
        choices = INTERESTED_FIELDS_CHOICES,
        blank = True, null = True
        )

    def get_absolute_url(self):
        '''
        This method when applied to Profile object in templates as
        object.get_absolute_url (default) will dynamically generate detail
        view url assosicated with profile username.
        '''
        return reverse('user_detail', kwargs={'username':self.user.username})

    def get_followers(self):
        return self.following.all()

    def get_followings(self):
        return Profile.objects.filter(followers=self).all()

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
        
    #     profile_img = Image.open(self.profile_picture.path)
        
    #     if profile_img.width > 400 or profile_img.height > 400:
    #         crop_size = (400,400)
    #         profile_img.thumbnail(crop_size)
    #         profile_img.save(self.profile_picture.path)

    def __str__(self):
        return f"{self.user.username}"


class Follow(models.Model):
    profile_from = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='follow_from',
    )
    profile_to = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='follow_to',
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        db_index=True)

        
    class Meta:
        ordering = ('-created_on',)


    def __str__(self):
        return f'{self.profile_from} follows {self.profile_to}'


