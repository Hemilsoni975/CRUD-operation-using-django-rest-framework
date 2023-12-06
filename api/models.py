from django.db import models

class notes(models.Model):
    SELECT_CHOICE = [
        ('publish', 'publish'),
        ('draft', 'draft')
    ]
    title = models.CharField(max_length=50, unique=True)
    desc = models.CharField(max_length=150, null=True)
    image = models.ImageField(upload_to='api/media/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=SELECT_CHOICE, default='active')

    # Use for ordering the items
    class Meta:
        ordering = ['title','id']


