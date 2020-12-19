# django model fields
from django.db import models

# factory settings
from django.conf import settings

# timezone
from django.utils import timezone

# reverse the parent content
from django.urls import reverse

# profile model
from profiles.models import Profile

# ckeditor field
from ckeditor.fields import RichTextField

# taggit manager for tagging bundles
from taggit.managers import TaggableManager

#slugify
from django.utils.text import slugify


class PublishManager(models.Manager):
    '''
    custom manager for filtering the bundles
    '''
    def get_queryset(self):
        return super(PublishManager,self).get_queryset().filter(status='Publish')

class ForkableManager(PublishManager):
    def get_queryset(self):
        return super(ForkableManager,self).get_queryset().filter(forkable=True)

class Bundle(models.Model):
    '''
    Bundle specifies a Bundle table in the database. 
    It consists of following attributes:
    - creator: foreign key to the Profile which owns the Bundle.
    - title : title is the title with which the bundle is created
    - context: RichTextField is from ckeditor
    - created_on: consists of time field when for first time the bundle is saved
    - publised_on: consists of time field to track the time when bundle is published
    - updated_on: consists of time field to track the time when bundle is updated
    - status: Default is set Draft, takes value from STATUS_CHOICES
    - media_image: images get saved in the project root_directory/media/bundle_image

    Attribute supporters:
    - STATUS_CHOICES: tuple of choices seperates bundle from being draft or publised 
    - objects: default manager which returns all objects
    - published: custom manager which return object filtered as Publish
    - tags: tags related to the bundle
    '''

    STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Publish', 'Publish'),
        )

    creator = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE,
        related_name='bundle_creator',
        )
    co_authors = models.ManyToManyField(
        Profile,
        through='AcceptedAuthorshipRequest', 
        related_name='cocreators',
        symmetrical=False
        ) 
    co_authors_request =  models.ManyToManyField(
        Profile,
        through='ReceivedAuthorshipRequest', 
        related_name='creatorrequests',
        symmetrical=False
        )       
    title = models.CharField(max_length=200)
    context = RichTextField(blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    published_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices = STATUS_CHOICES,
        default='Draft'
        )
    media_image = models.ImageField(
        upload_to='bundle_image',
        blank=True,
        null=True
        )
    media_file = models.FileField(
        upload_to='bundle_papers/%Y/%m/%d/',
        blank=True,
        null=True
        )
    slug = models.SlugField(null=False, unique=True)
    git_url = models.URLField(blank=True)
    forkable = models.BooleanField(default=False)
    fork = models.ManyToManyField(
        'self',
        through='Fork',
        related_name='forks',
        symmetrical=False
        )
    claps = models.ManyToManyField(
        Profile,
        through='Clap',
        related_name='bundle_liked',
        blank=True
        )
    #managers
    objects = models.Manager() 
    published = PublishManager() 
    fork_able = ForkableManager() 
    tags = TaggableManager()
    
    class Meta:
        '''
        modifiable meta class as per desire
        '''
        ordering = ('-published_on','title','context')

    
    def __str__(self):
        '''
        Returns object's title
        '''
        return self.title

    
    def get_absolute_url(self):
        '''
        This method when applied to Bundle object in templates as
        object.get_absolute_url (default) will dynamically generate detail
        view url assosicated with bundle creator's profile username.
        '''
        return reverse('detail_bundle', kwargs={'creator':self.creator,'slug': self.slug,})

    def get_forked_children(self):
        return self.fork.all()

    def get_forked_from(self):
        return Bundle.objects.filter(forks=self).all()    

    def get_author_requests(self):
        return self.co_authors_request.all()

    def get_co_authors(self):
        return self.co_authors.all()    

    def save(self, *args, **kwargs): 
        '''
        over riding the parent save method for
        dyanmically generate slug field from 
        the object's title
        '''
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Fork(models.Model):
    bundle_to = models.ForeignKey(
        Bundle,
        on_delete=models.CASCADE,
        related_name='forked_into',
    )
    bundle_from = models.ForeignKey(
        Bundle,
        on_delete=models.CASCADE,
        related_name='fork_origin',
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        db_index=True)

        
    class Meta:
        ordering = ('-created_on',)


    def __str__(self):
        return f'{self.bundle_from} forked into {self.bundle_to}'


class Clap(models.Model):
    bundle = models.ForeignKey(
        Bundle,
        on_delete=models.CASCADE,
        related_name='bundle',
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    claped_on = models.DateTimeField(
        auto_now_add=True,
        db_index=True)

        
    class Meta:
        ordering = ('-claped_on',)


    def __str__(self):
        return f'{self.profile} claped {self.bundle}'


# class AuthorshipRequestBase(models.Model):
#     bundle = models.ForeignKey(
#         Bundle,
#         on_delete=models.CASCADE, 
#         related_name='%(app_label)s_%(class)s_bundle',
#         )    
#     profile = models.ForeignKey(
#         Profile,
#         on_delete=models.CASCADE,
#         related_name='%(app_label)s_%(class)s_profile'
#         )
#     requested_on = models.DateTimeField(
#                 auto_now_add=True,
#                 db_index=True
#                 )

#     class meta:
#         abstract = True


class AcceptedAuthorshipRequest(models.Model):
    bundle = models.ForeignKey(
        Bundle,
        on_delete=models.CASCADE, 
        related_name='accepted_bundle',
        )    
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='accepted_profile'
        )
    accepted_on = models.DateTimeField(
                auto_now_add=True,
                db_index=True
                )

    def __str__(self):
        return f"{self.profile} is co-author to {self.bundle}"

class ReceivedAuthorshipRequest(models.Model):
    bundle = models.ForeignKey(
        Bundle,
        on_delete=models.CASCADE, 
        related_name='request_bundle',
        )    
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='request_profile'
        )
    requested_on = models.DateTimeField(
                auto_now_add=True,
                db_index=True
                )

    def __str__(self):
        return f"Received request of authorship to {self.bundle} from {self.profile}"


class Comment(models.Model):
    '''
    Comment specifies the Comment tabel in the database
    It consists of following attributes:
    - bundle: foreign key to the bundle the comment is being refered to
    - creator: foreign key to the Profile the comment is being created by 
    - title : title is the title with which the bundle is created
    - context: context is a text field for now, consists of long typeable text field
    - creation_date: consists of time field
    '''
    bundle = models.ForeignKey(
        Bundle, 
        on_delete=models.CASCADE, 
        related_name='comment',
        )
    creator = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE,
        null=True,
        related_name='comment_profile'
        )
    context = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_on']


    def __str__(self):
        return f"{self.creator} : {self.context}"