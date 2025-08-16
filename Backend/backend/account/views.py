# ========================================
#    NestJS vs Django: ফাইল স্ট্রাকচার এবং পার্থক্য
# ========================================


# ========================================


#+-------------------+----------------------------------------+------------------------------------------------------
#|     ফিচার          |               NestJS                   |               Django                                 |
#+===================+========================================+=======================================================
#|   Controller      | URL Routing এবং Request Handling       | Views সাধারণত HTML Template Rendering                 |
#                    | করা হয় কন্ট্রোলারের মধ্যে।                       এবং HTTP Response এর জন্য ব্যবহৃত হয়।
#+-------------------+----------------------------------------+------------------------------------------------------
#|   Service         | Business Logic এখানে থাকে। যেমন ডেটাবেস    | Django তে business logic সাধারণত                      |
#                    | থেকে ডেটা আনা, বা অন্য সিস্টেমে API কল করা।     views.py বা models.py তে থাকে।
#+-------------------+----------------------------------------+------------------------------------------------------
#|   Model           | ORM এর মাধ্যমে ডেটাবেস ম্যানেজ করা হয়।         | Django তে models.py ফাইলে থাকে এবং Django             | 
#                    | যেমন TypeORM, Sequelize।                  এর ORM ব্যবহার করে ডেটাবেস ম্যানেজ হয়।
#+-------------------+---------------------------- ------------+-----------------------------------------------------
#|   Routing         | রাউটিং controller ফাইলের মধ্যে থাকে এবং      | Django তে urls.py ফাইলে থাকে এবং views.py             |
#                    | URL module এর সাথে সংযুক্ত হয়। ডেকোরেটরের      ফাইলের মাধ্যমে response দেখানো হয়। 
#                    | মাধ্যমে পরিচালিত হয়। 
#+-------------------+-----------------------------------------+-----------------------------------------------------
#|   Template        | টেমপ্লেট সেবা NestJS এ views/ controllers   | Django তে templates/ controllers এর মাধ্যমে           |
#                    | মাধ্যমে সরবরাহ করা হয়।                        সরবরাহ করা হয়। 
#+-------------------+-----------------------------------------+-----------------------------------------------------
#|   Migration       | মাইগ্রেশন সেবা TypeORM বা Sequelize এর       | Django তে migrations/ কোডের মাধ্যমে এবং manage.py      |
#                    | মাধ্যমে হয় এবং migration ব্যবহার করা হয়।         এর মাধ্যমে মাইগ্রেশন ফোল্ডারে পরিচালিত হয়| 
#+-------------------+-----------------------------------------+-----------------------------------------------------
#|   Authentication  | NestJS এ JWT এবং OAuth ইনটিগ্রেশন ব্যবহার     | Django তে Django's authentication system           |
#                    | করে authentication করা হয়।                  বা JWT ব্যবহার করা হয়। 
#+-------------------+------------------------------------------+----------------------------------------------------
#|   Testing         | Unit Testing এবং Integration Testing     | Django তে tests.py ফাইলের মাধ্যমে এবং                  |
#                    | Jest তে Mocha এর সাথে ব্যবহার হয়।              Django Test Client ব্যবহার হয়। 
#+-------------------+------------------------------------------+----------------------------------------------------


from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
#kind of controller--->
# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

#new password
class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)






