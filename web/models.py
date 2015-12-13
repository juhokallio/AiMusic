from django.db import models
from django_pgjson.fields import JsonField


class Composer(models.Model):
    name = models.CharField(max_length=30)


class Composition(models.Model):
    composer = models.ForeignKey(Composer, related_name='compositions')
    name = models.CharField(max_length=30)
    music = JsonField()


class Critic(models.Model):
    composition = models.ForeignKey(Composition, related_name="critics")
    critic = JsonField()


class MusicConcept(models.Model):
    composer = models.ForeignKey(Composer)
    name = models.CharField(max_length=30)


class Midi(models.Model):
    data = models.BinaryField()
    composition = models.ForeignKey(Composition, related_name="midi")
