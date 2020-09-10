# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models
from PIL import Image
from django.core.validators import RegexValidator

# Create your models here.
def upload_update_image(instance, filename):
    return "profile_pics/{user}/{filename}".format(user=instance.user, filename=filename)
class profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,related_name="userAssociated")
    image= models.ImageField(default='profile_pics/default.jpg',upload_to=upload_update_image)
    
    phone_message = 'Phone number must be entered in the format: 917657468565' 

     # your desired format 
    phone_regex = RegexValidator(
        regex=r'^(91)\d{10}$',
        message=phone_message
    )

    # finally, your phone number field
    phone = models.CharField(validators=[phone_regex], max_length=60,
                             null=True, blank=True)
    def __str__(self):
        return self.user.username +' Profile'
    def save(self,*args,**kwargs):
        super(profile,self).save(*args,**kwargs)
        if self.image:
            image =Image.open(self.image.path)
            if image.height >300 or image.width >300:
                output_size=(300,300)
                image.thumbnail(output_size)
                image.save(self.image.path)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        p=profile(user=instance)
        p.save()

