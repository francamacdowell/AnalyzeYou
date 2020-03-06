from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from .models import *
from .serializer import *
from .resources.set_setup import SetSetup


class ChannelDetailsView(APIView):
    def get(self, format=None):
        queryset = ChannelDetails.objects.all()
        serializer = ChannelDetailsSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, data):
        serializer = ChannelDetailsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

    def delete(self, format=None):
        queryset = ChannelDetails.objects.all()
        serializer = ChannelDetailsSerializer(queryset, many=True)

        for i in serializer.data:
            pk = dict(i)
            element = ChannelDetails.objects.get(pk=pk['id'])
            element.delete()
        return Response(serializer.data)


class VideoDetailsView(APIView):
    def get(self, format=None):
        queryset = VideoDetails.objects.all()
        serializer = VideoDetailsSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, data):
        serializer = VideoDetailsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


class StatisticsDetailsView(APIView):
    def get(self, format=None):
        queryset = StatisticsDetails.objects.all()
        serializer = StatisticsDetailsSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, data):
        serializer = StatisticsDetailsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


class SetupView(APIView):
    def get(self, format=None):
        queryset = Setup.objects.all()
        serializer = SetupSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        self.delete()
        serializer = SetupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

        setup = SetSetup(serializer.data['link_video'])
        setup.init_api()
        ChannelDetailsView().post(setup.channel_details())
        StatisticsDetailsView().post(setup.statistics_details())
        VideoDetailsView().post(setup.video_details())

        return Response(serializer.data)

    def delete(self, format=None):
        queryset = Setup.objects.all()
        serializer = SetupSerializer(queryset, many=True)

        for i in serializer.data:
            pk = dict(i)
            element = Setup.objects.get(pk=pk['id'])
            element.delete()
        return Response(serializer.data)