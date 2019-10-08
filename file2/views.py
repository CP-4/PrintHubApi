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

from file2.models import Document
from file2.serializers import DocumentSerializer, TokenSerializer

import zipfile
import re
import xml.dom.minidom

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
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        # return Response("Bhagwan sab deek raha hai")
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)

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
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")

        if not username and not password and not email:
            return Response(
                data={
                    "message": "username, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            username=username, password=password, email=email
        )
        return Response(status=status.HTTP_201_CREATED)



class ListDocumentView(generics.ListAPIView):

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (permissions.AllowAny,)
    # permission_classes = (permissions.IsAuthenticated,)


class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET songs/:id/
    PUT songs/:id/
    DELETE songs/:id/
    """
    permission_classes = (permissions.AllowAny,)
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
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.AllowAny,)

    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

        try:
            serializer = DocumentSerializer(data=request.data)
            if serializer.is_valid():
                print("is_valid")
                serializer.save()
            else:
                print('not_valid')

            return Response(serializer.data, status=status.HTTP_201_CREATED)

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
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.AllowAny,)

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def put(self, request, *args, **kwargs):
        try:

            printTrayIds = list(request.data)
            print(printTrayIds)

            for id in printTrayIds:
                a_doc = self.queryset.get(pk=id)
                a_doc.printJobStatus = 1
                a_doc.save()

            return Response("Gotcha brother ;)")
        except Document.DoesNotExist:
            return Response(
                data={
                    "message": "Document with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class PickUpFiles(generics.RetrieveUpdateAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.AllowAny,)
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
            deliveryjobs = list(filter(lambda x: x.printJobStatus == 1, self.queryset.all()))
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
            deliveryjobs = list(filter(lambda x: x.printJobStatus == 3, self.queryset.all()))
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
