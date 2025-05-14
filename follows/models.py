from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.constraints import UniqueConstraint

User = get_user_model()


class Follow(models.Model):
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    followed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followed"
    )
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["follower", "followed"], name="unique_follow")
        ]

    def __str__(self):
        return f"{self.following} follows {self.followed}"
