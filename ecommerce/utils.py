import random 
import string
from django.utils.text import slugify
from datetime
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








def unique_activation_key_generator(instance,new_activation_key=None):
      print('unique activation key  generator')
      if new_activation_key is not None:
            activation_key=new_activation_key
      else:
            activation_key = slugify(random_string_generator())

      Klass=instance.__class__
      qs_exists=Klass.objects.filter(key=activation_key).exists()

      if qs_exists:
            size=random.randint(30,45)
            new_activation_key=f"{activation_key}-{random_string_generator(size=size)}"

            return unique_activation_key_generator(instance,new_activation_key=new_activation_key)
      
      return activation_key




def get_filename(filename):
      return os.path.basename(filename)





def get_last_month_data(today):
      """
      simple method to get the ddatetime objects for the start and end of last month 
      """
      this_month_data=datetime.datetime(today.year,today.month,1) #first day of this month
      last month_end=this_month_start - datetime.timedelta(days=1)
      last_month_start=datetime.datetime(last_month_end.year,last_month_end.month,1) #first day of previous month
      return (last_month_start,last_month_end)




def get_month_data_range(months_ago=1,include_this_month=False):
      """
      a method that generates a list of dictionaries that describe any given amount of monthly data
      """
      today=datetime.datetime.now().today
      dates_=[]
      if include_this_month:
            next_month = today.replace(day=28)+datetime.timedleta(days=4)
            start,end=get_last_month_data(next_month)
            dates_.insert(0,{
                  "start":start.timestamp(),
                  "end":end.timestamp(),
                  "start_json":start.isoformat(),
                  "end":end.timestamp(),
                  "end_json":end.isoformat(),
                  "timesince":0,
                  "year":start.year,
                  "month":str(start.strftime("%B")),
            })
            for x in range(0, months_ago):
                  start,end=get_last_month_data(today)
                  today=start
                  dates_.insert(0,{
                  "start":start.timestamp(),
                  "end":end.timestamp(),
                  "start_json":start.isoformat(),
                  "end":end.timestamp(),
                  "end_json":end.isoformat(),
                  "timesince":0,
                  "year":start.year,
                  "month":str(start.strftime("%B")),
                  })
            return dates_