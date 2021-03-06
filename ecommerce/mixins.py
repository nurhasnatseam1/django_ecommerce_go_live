from django.utils.http import is_safe_url
class NextUrlMixin(object):
      def get_next_url(self):
            request=self.request 
            next_=request.GET.get('next')
            next_post=request.POST.get('next')
            redirect_path = next_ or next_post 

            if is_safe_url(redirect_path,request.get_host()):
                  return redirect_path 
            return '/'