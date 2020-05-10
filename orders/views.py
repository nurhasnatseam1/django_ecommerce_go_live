from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.http import Http404 ,HttpResponse
from django.views.generic import View, ListView, DetailView 
from django.shortcuts import render 
from django.contrib import messages




# Create your views here.
import os 
from wsgiref.util import FileWrapper 
from django.conf import settings 
from mimetypes import guess_type
from products.mdoels import 


from billing.models import BillingProfile 
from .models import Order, ProductPurchase 



class OrderListView(LoginRequiredMixin,ListView):


      def get_queryset(self):
            return Order.objects.by_request(self.request).not_created()

class OrderDetailView(LoginRequiredMixin,DetailView):
      def get_object(self):
            qs=Order.objects.by_request(
                  self.request
            ).filter(order_id=self.Kwargs.get('order_id'))

            if qs.count()==1:
                  return qs.first()
            return Http404



def order_sucess(request):
      return render(request,"orders/success.html",{})




class LibraryView(LoginRequiredMixin,ListView):

      template_name='orders/library.html'

      def get_queryset(self):
            return ProductPurchase.objects.products_by_request(self.request)





class ProductDownloadView(View):
      def get(self,*args,**kwargs):
            slug=kwargs.get('slug')
            pk=kwargs.get('pk')
            qs=Product.objects.filter(slug=slug)
            if qs.count()!=1:
                  raise Http404("Product not found")
            product_obj=qs.first()
            downloads_qs=product_obj.get_downloads().filter(pk=pk)
            if downloads_qs.count() != 1:
                  raise Http404("downloads not found")
            download_obj=downloads_qs.first()
            #permission check
            can_download=False
            user_ready=True #to download the files
            if download_obj.user_required :
                  if request.user.is_authenticated():
                        user_ready=False
            purched_products=Product.objects.none()
            if download_obj.free:
                  can_download=True
                  user_ready=True
            else:
                  purchased_products=ProductPurchase.objects.products_by_request(request)#returns all the products owned by this billing_profile
                  if download_obj.product in purchased_products:
                        can_download=True

            if not can_download or not user_ready:
                  messages.error(request,"the request file is not download able ")
                  return redirect(download_obj.get_default_url())

            #to let consumer download a file you need to open file in ram to read it's binary representation and then send it to the user with response

            protected_root=settings.protected_root
            obj_file_path=download_obj.file.path 
            final_path=os.path.join(file_root,filepath)
            #final_path is where the file is stored no matter if it is on amazon or not

            with open(final_path,'rb') as f:
                  wrapper=FileWrapper(f)
                  mimetype='application/force-download'
                  guessed_mime_type=guess_type(filepath)[0]
                  if guessed_mime_type:
                        mimetype=guessed_mime_type

                  response =HttpResponse(wrapper,content_type=mimetype)
                  response['Content-Disposition']=f"attachment:filename={download_obj.name}"
                  response['X-SendFile']=str(download_obj.name)
                  return response

            return redirect(download_obj.get_default_redirect())





class VerifyOwnership(View):
      def get(self,request,*args,**kwargs):
            data=request.GET 
            product_id=request.GET.get('product_id')

            if product_id is not None:
                  product_id = int(product_id)
            ownership_ids=ProductPurchase.objects.products_ by_id(request)
            if product_id in ownership_ids:
                  return JsonResponse({'owner':True})
            return JsonResponse({'owner':False})
      raise Http404