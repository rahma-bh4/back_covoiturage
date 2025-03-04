from django.db import models
class User(models.Model):
    clerk_user_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.clerk_user_id
# Create your models here.
