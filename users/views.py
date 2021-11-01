

from datetime import datetime

# Create your views here.
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import *
from rest_framework import generics
from .serializers import *
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from datetime import datetime
from datetime import datetime
from rest_framework import permissions
import pdb


class CreateUser(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def post(self, request, format=None):
        result = {}
        result['status'] = 'NOK'
        result['valid'] = False
        result['result'] = {'message': 'Unauthorized', 'data': []}

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            result['status'] = 'OK'
            result['valid'] = True
            result['result']['message'] = "User created successfully !"
            return Response(result, status=status.HTTP_200_OK)
        else:
            result['result']['message'] = list(serializer.errors.keys())[
                0]+' - '+list(serializer.errors.values())[0][0]
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class Login (KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        result = {}
        result['status'] = 'NOK'
        result['valid'] = False
        result['result'] = {"message": "Unauthorized access", "data": []}

        if serializer.is_valid():
            try:
                user_data = authenticate(
                    email=serializer.validated_data['email'], password=serializer.validated_data['password'])

            except:
                # Response data
                result['status'] = 'NOK'
                result['valid'] = False
                result['result']['message'] = 'User not present'
                # Response data
                return Response(result, status=status.HTTP_204_NO_CONTENT)

            if user_data is not None:
                user_details = User.objects.all().filter(email=user_data).values(
                    'id', 'name', 'email', 'phone', 'registered_on', 'is_active')
                if user_data.is_active:
                    login(request, user_data)
                    data = super(Login, self).post(request)
                    data = data.data

                    data['user_info'] = user_details

                # Response data
                result['status'] = "OK"
                result['valid'] = True
                result['result']['message'] = "Login successfully"
                result['result']['data'] = data
                # Response data
                return Response(result, status=status.HTTP_200_OK)
            else:

                # Response data
                result['status'] = "NOK"
                result['valid'] = False
                result['result']['message'] = 'Invalid Credentials'
                # Response data
                return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # Response data
        result['status'] = "NOK"
        result['valid'] = False
        result['result']['message'] = list(serializer.errors.keys())[
            0]+' - '+list(serializer.errors.values())[0][0]
        
        return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class Logoutview(LogoutView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        result = {}
        result['status'] = 'NOK'
        result['valid'] = False
        result['result'] = {"message": "Unauthorized access", "data": []}

        if request.user.is_authenticated:
            try:
                request._auth.delete()
            except:
                # Response data
                result['status'] = "NOK"
                result['valid'] = False
                result['result']['message'] = 'Error while logging out'
                return Response(result, status=status.HTTP_200_OK)

            # Response data
            result['status'] = "OK"
            result['valid'] = True
            result['result']['message'] = 'Logout successfully !'
            # Response data
            return Response(result, status=status.HTTP_200_OK)


class ChangePassword(APIView):
    #permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request, format=None):
        result = {}
        result['status'] = "NOK"
        result['valid'] = False
        result['result'] = {"message": "Unauthorized access", "data": []}

        if request.user.is_authenticated:

            if request.user.is_anonymous:
                result['result']['message'] = "User Invalid"
                return Response(result, status=status.HTTP_200_OK)

            serializer = ChangePasswordSerializer(data=request.data)
            if serializer.is_valid():
                user = request.user

                if user.check_password(serializer.data['old_password']):
                    new_password = serializer.data['new_password']
                    user.set_password(serializer.data['new_password'])
                    request.user.save()

                # # Sending Mail of Login Activity
                #     ip = self.request.META.get('HTTP_X_FORWARDED_FOR', self.request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
                #     data = "ip address :  "+ str(ip)+ "\n"
                #     message =" Your Password was updated \n "
                #     date = "Updated Time:  " + str(datetime.now().strftime("%B %d %Y %H:%M:%S"))
                #     data = message + data + "new password:  "+str(new_password) + '\n' + date
                #     send_mail("Password Changed", data, "bhavanigloled@gmail.com", [user.email])
                # # Sending Mail Ends
                    al = {}
                    al['user_id'] = request.user.pk
                    al['operated_on'] = request.user.pk
                    al['activity_type'] = "Password Changed"
                    al['date_time'] = datetime.now()
                    al['ip_address'] = self.request.META.get(
                        'HTTP_X_FORWARDED_FOR', self.request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
                    serializer = LogTableSerializer(data=al)
                    if serializer.is_valid():
                        serializer.save()

                    # Response data
                    result['status'] = "OK"
                    result['valid'] = True
                    result['result']['message'] = "Password Changed"
                    # Response data
                    return Response(result, status=status.HTTP_201_CREATED)
                else:
                    result['result']['message'] = "Pasword did not match"
                    return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
