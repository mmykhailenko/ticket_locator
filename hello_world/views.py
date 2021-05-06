from hello_world.models import SearchHistory, User
from hello_world.serializers import SearchHistorySerializer
from rest_framework import generics


class SearchHistoryList(generics.ListCreateAPIView):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SearchHistoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer

