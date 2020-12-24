from django.contrib.auth.mixins import UserPassesTestMixin
from activities.utils import create_action
from events.models import Bundle,Fork
from profiles.models import Profile
from django.contrib.auth.models import User

class BundleEditMixin( UserPassesTestMixin ):
    def test_func(self):
        '''
        check if the creator of bundle is the one requesting to update it
        '''
        if Profile.objects.get(user=self.request.user) == self.get_object().creator:
            return True
        return False  


class UserIsOwnerMixin():
    def user_is_owner(self,obj_list):
        if (self.request.user.is_authenticated and 
            Profile.objects.get(user=self.request.user) 
                == Profile.objects.get(user=User.objects.get(username=self.kwargs['creator']))):
            '''
            check if the requesting user is the owner of the bundle
            if True return all private and public bundle for the
            requesting user
            '''
            return obj_list.filter(
                    creator=Profile.objects.get(user=User.objects.get(username=self.kwargs['creator']))
                    )
        else:
            '''
            if requesting user is not the owner of the bundle or
            is an anonymous user then return all public bundle
            of the provided username
            '''
            return obj_list.filter(
                    creator=Profile.objects.get(user=User.objects.get(username=self.kwargs['creator'])),
                    status='Publish') 


class CreateActivityMixin():
    def create_published_action(self):
        if self.object.status == 'Publish':
            create_action(Profile.objects.get(user=self.request.user), 'created a new bundle', self.object)

    def create_fork_action(self,bundle_from):
        create_action(Profile.objects.get(user=self.request.user), 'forked bundle', bundle_from)
    
    def create_comment_action(self,bundle_to_comment):
        create_action(Profile.objects.get(user=self.request.user), 'commented on bundle', bundle_to_comment)

    def create_clap_action(self,bundle_to_clap):
        create_action(Profile.objects.get(user=self.request.user), 'clapped the bundle', bundle_to_clap)  


class CreateForkMixin(): 
    def create_bundle_fork(self,bundle_from,new_owner):
        
        bundle_dict = bundle_from.get_dict()
        title = bundle_dict['title']
        slug = bundle_dict['slug'] + '-' + self.request.user.username
        context = bundle_dict['context']
        status = 'Publish'
        bundle_to = Bundle.objects.create(
                            creator = new_owner,
                            title = title,
                            slug = slug,
                            context = context,
                            status = status
                        ) 
        Fork.objects.create(
                        bundle_to = bundle_to,
                        bundle_from = bundle_from 
                        )
 