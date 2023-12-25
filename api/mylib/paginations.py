from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    invalid_page_message = "ops! page not foud :("
    page_size = 10
    max_page_size = 20
    page_query_param = 'page'