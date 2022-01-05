from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.name} ({self.address})'

class Participant(models.Model):
    email = models.EmailField(unique=True)
    

    def __str__(self):
        return self.email


# Create your models here.
class Meetup(models.Model):
    title = models.CharField(max_length=200)
    organizer_email = models.EmailField()
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    location = models.ForeignKey(Location, on_delete=models.SET_DEFAULT, default=1)
    participants = models.ManyToManyField(Participant, blank=True, null=True)
    date_sent = models.DateField()
    date_published = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.slug}'
