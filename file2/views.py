from django.shortcuts import render

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import generics
from rest_framework import permissions, status
from rest_framework.parsers import FileUploadParser

from file2.models import Document
from file2.serializers import DocumentSerializer


class ListDocumentView(generics.ListAPIView):

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET songs/:id/
    PUT songs/:id/
    DELETE songs/:id/
    """
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

    queryset = filter(lambda x: x.printJobStatus == 1, Document.objects.all())
    serializer_class = DocumentSerializer

class GetDeliveryJobs(generics.ListAPIView):

    queryset = filter(lambda x: x.printJobStatus == 3, Document.objects.all())
    serializer_class = DocumentSerializer
