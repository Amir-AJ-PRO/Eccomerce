from kavenegar import *
from django.contrib.auth.mixins import UserPassesTestMixin
def send_otp_code(phone , code):
    try:
        api = KavenegarAPI('616E43485062434C446E6764535567545A51394F59596A417A6B30746B783369687568564348667A45516F3D')
        params = { 'sender' : '200050066', 'receptor': phone , 'message' : f'کد شما {code}' }

        response = api.sms_send( params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)

class IsAdminUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin