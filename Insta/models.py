from django.db import models
from imagekit.models import ProcessedImageField
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

# Create your models here.
class InstaUser(AbstractUser):
	profile_image = ProcessedImageField(
		upload_to = 'static/image/profiles',
		format = 'JPEG',
		options = {'quality':100},
		blank = True,
		null = True
		)
	def get_connections(self):
		
		connections = UserConnection.objects.filter(creator=self)  #所有我创造的connection#
		return connections
	
	def get_followers(self):
		
		followers = UserConnection.objects.filter(following=self)
		return followers
		
	def is_followed_by(self, user):

		followers = UserConnection.objects.filter(following=self)
		return followers.filter(creator=user).exists()


class UserConnection(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friendship_creator_set")
    following = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friend_set")

    def __str__(self):
        return self.creator.username + ' follows ' + self.following.username

class Post(models.Model):
	author = models.ForeignKey(
		InstaUser,
		on_delete = models.CASCADE,
		related_name = 'my_posts')
	title = models.TextField(blank = True, null = True)
	image = ProcessedImageField(
		upload_to = 'static/image/posts',
		format = 'JPEG',
		options = {'quality':100},
		blank = True,
		null = True
		)
	def get_like_count(self):
		return self.likes.count()
		
	def get_absolute_url(self):
		return reverse("post_detail", args = [str(self.id)])#reverse 跳转到名称为()的url

class Like(models.Model):
	post = models.ForeignKey(
		Post,
		on_delete = models.CASCADE,
		related_name = 'likes')
	user = models.ForeignKey(
		InstaUser,
		on_delete = models.CASCADE,
		related_name = 'likes')

	class Meta(object):
		unique_together = ('post','user')

	def __str__(self):
			return 'Like: ' + self.user.username + ' likes ' + self.post.title
			