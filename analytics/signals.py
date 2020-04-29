from django.dispatch import Signal 





object_viewed_signal=Signal(providing_args=['instance','request'])  # unlike djnago default signals in custom signals  you have to provid the sender in signalInstance.send(instance.__class__,then the providing arguments) ,thats why in custom signalInstance.connect(only_receiver_function,do not need any sender)