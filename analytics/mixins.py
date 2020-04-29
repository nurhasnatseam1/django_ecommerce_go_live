from .signals import object_viewed_signal




class ObjectViewedMixin(object):
      def get_context_data(self,*args,**kwargs):
            context=super().get_context_data(*args,**kwargs)
            request=self.request 
            instance=context['object']
            object_viewed_signal.send(instance.__class__,instance=instance,request=request)
            return  context