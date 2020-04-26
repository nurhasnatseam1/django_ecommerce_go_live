import random 
import string
from django.utils.text import slugify

def random_string_generator(size=4,chars=string.ascii_lowercase+string.digits):
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
            new_slug=f"{slug}-{random_string_generator(size=4)}"

            return unique_slug_generator(instance,new_slug=new_slug)
      
      return slug


def unique_order_id_generator(instance,new_order_id=None):
      print('unique order id generator')
      if new_order_id is not None:
            order_id=new_order_id
      else:
            order_id = slugify(random_string_generator())

      Klass=instance.__class__
      qs_exists=Klass.objects.filter(order_id=order_id).exists()

      if qs_exists:
            new_order_id=f"{order_id}-{random_string_generator(size=4)}"

            return unique_order_id_generator(instance,new_order_id=new_order_id)
      
      return order_id