from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions

from django.shortcuts import render

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import generics
from rest_framework import permissions, status
from rest_framework.parsers import FileUploadParser
from rest_framework.parsers import JSONParser

import io

from file2.models import Document, CustomUser, UrlAnalytics, GuestStudent, Shop
from file2.serializers import DocumentSerializer, TokenSerializer, CustomUserSerializer, UrlAnalyticsSerializer, GuestStudentSerializer, ShopSerializer

import zipfile
import re
import xml.dom.minidom

from datetime import date

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# TODO: update all queryset

class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)
    queryset = CustomUser.objects.all()

    def post(self, request, *args, **kwargs):
        # return Response("Bhagwan sab deek raha hai")
        print(request.data)

        email = request.data.get("email", "")
        password = request.data.get("password", "")

        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class RegisterUsersView(generics.CreateAPIView):
    """
    POST auth/register/
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):

        print(request.data)

        student_name = request.data.get("student_name", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        phone = request.data.get("phone", "")

        regexEmail = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if(re.search(regexEmail, email)):
            print("email accepted")
            pass
        else:
            print("email rejected")
            email = ''

        regexPhone= '^[0-9]{10}$'
        if(re.search(regexPhone, phone)):
            print("phone accepted")
            pass
        else:
            print("phone rejected")
            phone = ''

        if not student_name or not password or not email or not phone:
            return Response(
                data={
                    "message": "Name, password, phone number and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = CustomUser.objects.create_user(
            student_name=student_name, password=password, email=email
        )

        new_user.phone = phone
        new_user.save()

        print(new_user)
        login(request, new_user)
        serializer = TokenSerializer(data={
            # using drf jwt utility functions to generate a token
            "token": jwt_encode_handler(
                jwt_payload_handler(new_user)
            )})
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_201_CREATED)



class ListDocumentView(generics.ListAPIView):

    # queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    # permission_classes = (permissions.AllowAny,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        This view should return a list of all the documents
        for the currently authenticated user.
        """
        user = self.request.user
        return Document.objects.filter(student=user)


class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET files/:id/
    PUT files/:id/
    DELETE files/:id/
    """
    permission_classes = (permissions.IsAuthenticated,)
    # permission_classes = (permissions.AllowAny,)
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_doc = self.queryset.get(pk=kwargs["pk"])
            # print(DocumentSerializer(a_doc).data)
            return Response(DocumentSerializer(a_doc).data)
        except Document.DoesNotExist:
            return Response(
                data={
                    "message": "Document with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            a_doc = self.queryset.get(pk=kwargs["pk"])
            serializer = DocumentSerializer()
            updated_document = serializer.update(a_doc, request.data)
            return Response(DocumentSerializer(updated_document).data)
        except Document.DoesNotExist:
            return Response(
                data={
                    "message": "Document with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_doc = self.queryset.get(pk=kwargs["pk"])
            a_doc.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Document.DoesNotExist:
            return Response(
                data={
                    "message": "Document with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class UploadDocumentView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    # permission_classes = (permissions.AllowAny,)

    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

        try:
            print(request.data)
            serializer = DocumentSerializer(data=request.data, context={'request': request})

            # print(request.data)
            if serializer.is_valid():
                print("is_valid")
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print('not_valid')
                print(serializer.errors)
                return Response('not_valid')


        except Document.DoesNotExist:
            return Response(
                data={
                    "message": "Document not uploaded"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class UpdatePrintStatusDone(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_doc = self.queryset.get(pk=kwargs["pk"])
            a_doc.printJobStatus = 2
            a_doc.save()
            return Response(DocumentSerializer(a_doc).data)
        except Document.DoesNotExist:
            return Response(
                data={
                    "message": "Document with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


    def put(self, request, *args, **kwargs):

        print(request.data)

        try:
            a_doc = self.queryset.get(pk=kwargs["pk"])
            a_doc.printJobStatus = request.data.get('printJobStatus')
            a_doc.save()
            return Response(DocumentSerializer(a_doc).data)

        except Document.DoesNotExist:
            return Response(
                data={
                    "message": "Document with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class PrintFiles(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    # permission_classes = (permissions.AllowAny,)

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def put(self, request, *args, **kwargs):
        try:
            print(request.data)

            printTray = list(request.data['print_tray'])
            promo_code = request.data['promo_code']

            # a_doc = self.queryset.get(pk=kwargs["pk"])
            # serializer = DocumentSerializer()
            # updated_document = serializer.update(a_doc, request.data)

            for document in printTray:
                a_doc = self.queryset.get(pk=document['id'])
                a_doc.printJobStatus = 1
                a_doc.print_feature = document['print_feature']
                a_doc.print_copies = document['print_copies']
                a_doc.print_cost = document['print_cost']
                shop = CustomUser.objects.get(pk=document['shop'])
                a_doc.shop = shop
                if promo_code:
                    a_doc.promo_code = promo_code

                a_doc.save()


            # for id in printTrayIds:
            #     a_doc = self.queryset.get(pk=id)
            #     a_doc.printJobStatus = 1
            #     a_doc.save()

            return Response("Gotcha brother ;)")
        except Document.DoesNotExist:
            return Response(
                data={
                    "message": "Document with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class PickUpFiles(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    # permission_classes = (permissions.AllowAny,)
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def put(self, request, *args, **kwargs):
        try:

            printTrayIds = list(request.data)
            print(printTrayIds)

            for id in printTrayIds:
                a_doc = self.queryset.get(pk=id)
                a_doc.printJobStatus = 3
                a_doc.save()

            return Response("Gotcha brother ;)")
        except Document.DoesNotExist:
            return Response(
                data={
                    "message": "Document with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class GetPrintJobs(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    # deliveryjobs = list(filter(lambda x: x.printJobStatus == 3, queryset.all()))
    # print(deliveryjobs)

    def get(self, request, *args, **kwargs):
        try:
            user = self.request.user
            # deliveryjobs = list(filter(lambda x: x.printJobStatus == 1, self.queryset.all()))
            deliveryjobs = list(filter(lambda x: x.printJobStatus == 1, self.queryset.filter(shop=user)))
            print(deliveryjobs)
            return Response(DocumentSerializer(deliveryjobs, many=True).data)
        except Document.DoesNotExist:
            return Response(
                data={
                    "message": "Some error occured"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class GetDeliveryJobs(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    # deliveryjobs = list(filter(lambda x: x.printJobStatus == 3, queryset.all()))
    # print(deliveryjobs)

    def get(self, request, *args, **kwargs):
        try:
            user = self.request.user
            deliveryjobs = list(filter(lambda x: x.printJobStatus == 3, self.queryset.filter(shop=user)))
            print(deliveryjobs)
            return Response(DocumentSerializer(deliveryjobs, many=True).data)
        except Document.DoesNotExist:
            return Response(
                data={
                    "message": "Some error occured"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class SetPrintJobStatus(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.AllowAny,)

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def put(self, request, *args, **kwargs):

        document_id = request.data.get('Id')
        printJobStatus = request.data.get('PrintJobStatus')

        print(document_id, printJobStatus)

        try:
            a_doc = self.queryset.get(pk=document_id)
            a_doc.printJobStatus = printJobStatus
            a_doc.save()
            return Response(DocumentSerializer(a_doc).data)

        except Document.DoesNotExist:
            return Response(
                data={
                    "message": "Document with id: {} does not exist".format(document_id)
                },
                status=status.HTTP_404_NOT_FOUND
            )


class TestUpdatePrintStatusDone(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    # queryset2 = Document.objects.filter(printJobStatus="1")
    serializer_class = DocumentSerializer


    # print(queryset2)

    def get(self, request, *args, **kwargs):
        try:
            queryset2 = Document.objects.filter(printJobStatus="1")
            queryset2.filter(printJobStatus="1")
            for job in queryset2:
                # print(job.id, job.printJobStatus)
                job.printJobStatus = 2
                # print(job.id, job.printJobStatus)
                job.save()

            return Response("All pending files printed ;)")

        except Document.DoesNotExist:
            return Response(
                data={
                    "message": "Document with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class UrlAnalyticsView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = UrlAnalytics.objects.all()
    serializer_class = UrlAnalyticsSerializer

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
            return ip

    def get(self, request, *args, **kwargs):
        ip = self.get_client_ip(request)
        print(ip)

        # anal = list(self.queryset.all())
        # print(anal)
        today = date.today()
        anal = list(UrlAnalytics.objects.filter(dtime__year=today.year, dtime__month=today.month, dtime__day=today.day))

        return Response(UrlAnalyticsSerializer(anal, many=True).data)

        # return Response(
        # data = self.serializer_class(self.queryset.all())
        # )

    def post(self, request, *args, **kwargs):
        try:
            a_url = UrlAnalytics.objects.create()
            ip = self.get_client_ip(request)
            print('============================')
            print(request.data)
            # print(user.email)

            a_url.data = request.data['data']
            a_url.temp_user_id = request.data['temp_user_id']

            try:
                user = request.user
                a_url.student_email = user.email
                pass
            except AttributeError:
                pass

            a_url.save()

            today = date.today()
            anal = list(UrlAnalytics.objects.filter(dtime__year=today.year, dtime__month=today.month, dtime__day=today.day))

            return Response(UrlAnalyticsSerializer(anal, many=True).data)

            # return Response(
            #     data={
            #     self.queryset.all()
            #     },
            #     status=status.HTTP_404_NOT_FOUND
            # )
        except Document.DoesNotExist:
            return Response(
                data={
                "message": "Some error occured"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class GuestStudentView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = GuestStudent.objects.all()
    serializer_class = GuestStudentSerializer

    def get(self, request, *args, **kwargs):
        guest = list(self.queryset.all())
        # print(anal)
        return Response(GuestStudentSerializer(guest, many=True).data)


    def post(self, request, *args, **kwargs):
        try:
            # print('1')
            a_user = GuestStudent.objects.create()
            # print('2')
            print(request.data)
            a_user.student_name = request.data['user_name']
            a_user.student_phone = request.data['user_phone']
            a_user.student_branch = request.data['user_branch']
            a_user.save()
            # print('3')
            # anal = list(self.queryset.all())
            # print(anal)
            return Response("Student registered")

            # return Response(
            #     data={
            #     self.queryset.all()
            #     },
            #     status=status.HTTP_404_NOT_FOUND
            # )
        except Document.DoesNotExist:
            return Response(
                data={
                "message": "Some error occured"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class UpdateStudentView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    # permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            print(request.data)
            print(request.user)

            a_user = self.request.user

            a_user.college = request.data['clg_value']
            a_user.branch = request.data['branch_value']
            a_user.year = request.data['year_value']
            # a_user.phone = request.data['phone_value']
            a_user.save()

            return Response("Profile updated")
        except Document.DoesNotExist:
            return Response(
                data={
                    "message": "Error occured"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class ListShopView(generics.ListAPIView):

    # queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = (permissions.AllowAny,)
    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        This view should return a list of all the shops.
        """
        # user = self.request.user
        # return Shop.objects.all()

        shops = Shop.objects.all()
        print(shops[0].user_id)
        return Response(ShopSerializer(shops, many=True).data)


class CreateShopView(generics.RetrieveUpdateAPIView):
    # permission_classes = (permissions.AllowAny,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:

            a_user = self.request.user
            data = request.data
            shop = a_user.shop_set.first()

            # if 'id' in data:
            #     shop = Shop.objects.get(pk=data['id'])

            if shop:
                serializer = ShopSerializer(shop, data=data, context={'request': request})

            else:
                serializer = ShopSerializer(data=data, context={'request': request})

            # print(request.data)
            if serializer.is_valid():
                print("is_valid")
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print('not_valid')
                print(serializer.errors)
                return Response('not_valid')

        except Shop.DoesNotExist:
            return Response(
                data={
                    "message": "Error occured"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class ShopDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET files/:id/
    PUT files/:id/
    DELETE files/:id/
    """
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.AllowAny,)
    # queryset = Document.objects.all()
    # serializer_class = DocumentSerializer

    def get(self, request, *args, **kwargs):
        try:
            shop = Shop.objects.get(pk=kwargs["pk"])
            # print(DocumentSerializer(a_doc).data)
            return Response(ShopSerializer(shop).data)
        except Document.DoesNotExist:
            return Response(
                data={
                    "message": "Shop with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class ShopDetailFromUserView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            user = self.request.user
            shop = user.shop_set.first()
            print(shop.id, shop.name)

            if shop:
                return Response(ShopSerializer(shop).data)
            else:
                return Response(
                    data={
                        "message": "No shop associated with this account, please fill Shop Detials"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        except Document.DoesNotExist:
            return Response(
                data={
                    "message": "Shop with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
