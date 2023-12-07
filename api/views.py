import logging

from rest_framework.response import Response

import api
from .models import notes
from .serializer import noteSerializer
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.generics import ListCreateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView

from .utils import success_true_response, success_false_response


# Configure logging
logger = logging.getLogger("api.views")

# Create your views here.

# pagination

# number pagination
# limitoffetpagination
# class StandardResultSetPagination(PageNumberPagination):
#     page_size = 5
#     page_query_param = 'p'
#     max_page_size = 100


# cursor pagination
class MyCursorPagination(CursorPagination):
    page_size = 5
    ordering = 'title'

class notesViewSet(viewsets.ModelViewSet, GenericAPIView):
    queryset = notes.objects.all()
    serializer_class = noteSerializer

    ordering_fields = ['id','title']

    # pagination
    # pagination_class = StandardResultSetPagination
    # cursor pagination
    pagination_class = MyCursorPagination

    # for filtering

    # filtering with draft or published #publish=@ps12345678 #draft=@ds12345678
    # def get_queryset(self):
    #     user = self.request.user
    #     return notes.objects.filter(status=user)
    #   or

    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ['status']

    # search filter
    search_fields = ['status']
    # search_fields = ['^title']

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            # Perform additional filtering based on query parameters
            # For example, you can filter based on a request parameter named 'active'
            active_filter = request.query_params.get('active')
            if active_filter:
                queryset = queryset.filter(active=active_filter)

                # Perform ordering based on request parameter 'ordering'
            ordering = request.query_params.get('ordering')
            if ordering in self.ordering_fields:
                queryset = queryset.order_by(ordering)

            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                logger.info('Data listed successfully')
                return self.get_paginated_response(
                    success_true_response(message='Data retrieved successfully', data=serializer.data))

            serializer = self.get_serializer(queryset, many=True)
            logger.info('Data listed successfully')
            return Response(success_true_response(message='Data retrieved successfully', data=serializer.data))
        except Exception as e:
            logger.error(f"An error occurred during listing: {e}")
            return Response(success_false_response(message='Failed to retrieve data', data={'error': str(e)}))

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            logger.info('Note created successfully')  # Log info message
            return Response(success_true_response(message='Note created successfully', data={"Success":serializer.data},))
        except Exception as e:
            logger.error(f"An error occurred during creation: {e}")  # Log error message
            return Response(success_false_response(message='Failed to create Note', data={'error': str(e)}),
                                status=400)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            logger.info('Note updated successfully')  # Log info message
            return Response(success_true_response(message='Note updated successfully'))
        except Exception as e:
            logger.error(f"An error occurred during update: {e}")  # Log error message
            return Response(success_false_response(message='Failed to update Note', data={'error': str(e)}),
                                status=400)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            logger.info('Note deleted successfully')  # Log info message
            return Response(success_true_response(message='Note deleted successfully'))
        except Exception as e:
            logger.error(f"An error occurred during deletion: {e}")  # Log error message
            return Response(success_false_response(message='Failed to delete Note', data={'error': str(e)}),
                                status=400)