import stripe
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save,pre_save
from accounts.models import GuestEmail
# Create your models here.



User=get_user_model()
stripe.api_key='sk_test_HwvAUIsohGImpP7zwFEZvO6q00xd5DlMjJ'

#an unauthenticated user can have 100000 billing profiles
#but an authenticated user can only have one billing profile
#if an unauthenticated user having many billing profile gets authenticated for the first time
#then all his billing profile with the email should get deactivated

class BillingProfileManager(models.Manager):

      def new_or_get(self,request):
            user=request.user
            guest_email_id=request.session.get('guest_email_id')
            if user.is_authenticated:
                  if user.email:
                        billing_profile,billing_profile_created=self.model.objects.get_or_create(user=user,email=user.email)
            elif guest_email_id:
                  guest_email=GuestEmail.objects.filter(id=guest_email_id).order_by("-timestamp").first()
                  billing_profile,billing_profile_created=self.model.objects.get_or_create(email=guest_email.email)
            else:
                  billing_profile=None
                  billing_profile_created=None

            return billing_profile,billing_profile_created




class BillingProfile(models.Model):
    user=models.ForeignKey(User,unique=True,on_delete=models.CASCADE,null=True,blank=True,related_name="billingProfile")
    email=models.EmailField()
    timestamp=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)
    #customer id from stripe or brain tree
    customer_id=models.CharField(max_length=120,null=True,blank=True)


    objects=BillingProfileManager()
    def __str__(self):
        return self.email

    def charge(self,order_obj,card=None):
        return Charge.objects.do(self,order_obj,card)

    def set_cards_inactive(self):
        cards_qs=self.get_cards()
        cards_qs.update(active=False)
        return cards_qs.filter(active=True).count()

    @property
    def has_card(self):
        instance=self 
        card_qs=instance.card_set.all()
        return card_qs.exists()
    def get_cards(self):
        return self.card_set.all()
    @property
    def get_default_card(self):
        card_qs=self.get_cards()
        return card_qs.filter(default=True,active=True).first()





def billing_profile_created_receiver(sender,instance,*args,**kwargs):
    if not instance.customer_id and instance.email:
        print('send request to stripe to create a new user and give us the customer id')
        customer=stripe.Customer.create(email=instance.email)
        instance.customer_id = customer.id


pre_save.connect(billing_profile_created_receiver,sender=BillingProfile)




def user_created_receiver(sender,instance,created,*args,**kwargs):
      if created:
            BillingProfile.objects.get_or_create(user=instance,email=instance.email)


      return None


post_save.connect(user_created_receiver,sender=User)


class CardManager(models.Manager):
    def all(self,*args,**kwargs):
        return self.get_queryset().filter(active=True)
    
    def add_new(self,billing_profile,token=None):
        if token is not None:
            customer=stripe.Customer.retrieve(billing_profile.customer_id)
            card_information=customer.sources.create(source=token)
            stripe_card=card_information
            if str(stripe_card.object)=="card":
                new_card=self.model(
                billing_profile=billing_profile,
                stripe_card_id=stripe_card.id, #cart.id is the (token) for the cart
                brand=stripe_card.brand,
                country=stripe_card.country,
                exp_month=stripe_card.exp_month,
                exp_year=stripe_card.exp_year,
                last4=stripe_card.last4
                )
                new_card.save()
                return new_card
            return None


class Card(models.Model):
    billing_profile=models.ForeignKey(BillingProfile,on_delete=models.CASCADE)
    stripe_card_id = models.CharField(max_length=120,null=True,blank=True) #stripe card id for this customer
    brand   =models.CharField(max_length=120,null=True,blank=True)
    country=models.CharField(max_length=20,null=True,blank=True)
    exp_month=models.IntegerField(null=True,blank=True)
    exp_year=models.IntegerField(null=True,blank=True)
    last4=models.CharField(max_length=20,null=True,blank=True)
    default=models.BooleanField(default=True)
    active=models.BooleanField(default=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    objects=CardManager()

    def __str__(self):
        return f"{self.stripe_card_id} last4:{self.last4}"



def post_save_card_receiver(sender,instance,created,*args,**kwargs):
    if instance.default:
        billing_profile=instance 
        qs=Card.objects.filter(billing_profile=billing_profile).exclude(pk=instance.pk)
        qs.update(default=False)



post_save.connect(post_save_card_receiver,sender=Card)


class ChargeManager(models.Manager):
    def do(self,billing_profile,order_obj,card=None):
        card_obj=card
        if card_obj is None:
            cards=billing_profile.card_set.filter(default=True)
            if cards.exists():
                card_obj=cards.first()
        if card_obj is None:
            return False, "No cards Available"
        charge=stripe_charge=stripe.Charge.create(
            amount=int(order_obj.order_total*100), #pass dollar in cents
            currency='usd',
            customer=billing_profile.customer_id,
            source=card_obj .stripe_card_id,
            description=f"Charge for {billing_profile.email}",
            metadata={
                'order_id':order_obj.order_id
            }
        )

        new_charge_obj=self.model.objects.create(
        billing_profile=billing_profile,
        stripe_card_id=charge.id,
        paid=charge.paid,
        refunded=charge.refunded,
        outcome=charge.outcome,
        outcome_type=charge.outcome.get('type'),
        seller_message=charge.outcome.get('seller_message'),
        risk_level=charge.outcome.get('risk_level'),
        )

        return new_charge_obj.paid,new_charge_obj.seller_message


class Charge(models.Model):
    billing_profile     =models.ForeignKey(BillingProfile,on_delete=models.DO_NOTHING)
    stripe_card_id      =models.CharField(max_length=120)
    paid                =models.BooleanField(default=True)
    refunded            =models.BooleanField(default=True)
    outcome             =models.TextField(null=True,blank=True)
    outcome_type        =models.CharField(max_length=120,null=True,blank=True)
    seller_message      =models.CharField(max_length=120,null=True,blank=True)
    risk_level          =models.CharField(max_length=120,null=True,blank=True)


    objects=ChargeManager()


    def __str__(self):
        return f"card_id:{self.stripe_card_id} outcome={self.outcome}"
