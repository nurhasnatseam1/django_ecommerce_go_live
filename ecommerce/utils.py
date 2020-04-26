import random 
import string
from django.utils.text import slugify

def random_stirng_generator(size=4,chars=string.ascii_lowercase+string.digits):
      return ''.join(random.choice(chars) for _ in range(size))



def unique_slug_generator(instance,new_slug=None):
      print('unique slug generator')
      if new_slug is not None:
            slug=new_slug
      else:
            slug = slugify(instance.title)

      Klass=instance.__class__
      qs_exists=Klass.objects.filter(slug=slug).exists()

      if qs_exists:
            new_slug=f"{slug}-{random_stirng_generator(size=4)}"

            return unique_slug_generator(instance,new_slug=new_slug)
      
      return slug