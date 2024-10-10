import uuid
from django.utils.timezone import now
from .models import VisitorLog  

class TrackVisitorMiddleware: 
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            visitor_id = request.COOKIES.get('visitor_id')

            if visitor_id:
                self.associate_visitor_to_user(request.user, visitor_id, request)
                response = self.get_response(request)
                response.delete_cookie('visitor_id')
            else:
                response = self.get_response(request)
        else:
            visitor_id = request.COOKIES.get('visitor_id')

            if not visitor_id:
                visitor_id = str(uuid.uuid4())
                response = self.get_response(request)
                response.set_cookie('visitor_id', visitor_id, max_age=60*60*24*365)  #1yr
            else:
                response = self.get_response(request)

            self.log_visitor_action(visitor_id, request.path, request.method, request)

        return response

    def log_visitor_action(self, visitor_id, path, method, request):        
        ip_address = self.get_ip_address(request)
        if not VisitorLog.objects.filter(visitor_id=visitor_id, path=path, method=method, ip_address=ip_address).exists():
            VisitorLog.objects.create(
                visitor_id=visitor_id,
                path=path,
                method=method,
                ip_address=ip_address,
                timestamp=now()
            )

    def associate_visitor_to_user(self, user, visitor_id, request):       
        ip_address = self.get_ip_address(request)
        VisitorLog.objects.filter(visitor_id=visitor_id, user__isnull=True).update(user=user, ip_address=ip_address)

    def get_ip_address(self, request):     
      
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip:
          
            ip = ip.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
