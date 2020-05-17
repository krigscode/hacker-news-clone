from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class LinkVoteCountManager(models.Manager):
    def get_query_set(self):
        return super(LinkVoteCountManager, self).get_query_set().annotate(votes=Count('vote')).order_by('-votes', '-rank_score')

class Link(models.Model):
    title = models.CharField("Headline", max_length=100)
    submitter = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    submitted_on = models.DateTimeField(auto_now_add=True)
    rank_score = models.FloatField(default=0.0)
    url = models.URLField("URL", max_length=250, blank=True)
    description = models.TextField(blank=True)
    with_votes = LinkVoteCountManager()
    objects = models.Manager() #default manager
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("link_detail", kwargs={"pk": str(self.id)})
    def set_rank(self):
        # Based on HN ranking algo at http://amix.dk/blog/post/19574
        SECS_IN_HOUR = float(60*60)
        GRAVITY = 1.2
        delta = now() - self.submitted_on
        item_hour_age = delta.total_seconds() // SECS_IN_HOUR
        votes = self.votes - 1
        self.rank_score = votes / pow((item_hour_age+2), GRAVITY)
        self.save()
    def approved_comments(self):
        return self.comments.filter(approved_comment=True)
        
class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name="votes")

    def __str__(self):
        return "%s upvoted %s" % (self.voter.username, self.link.title)

class UserProfile(models.Model):
        user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
        bio = models.TextField(null=True)

        def __str__(self):
            return "%s's profile" % self.user

def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

class Comment(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    def __str__(self):
        return self.text

    def approve(self):
        self.approved_comment = True
        self.save()

# Signal while saving user
post_save.connect(create_profile, sender=User)