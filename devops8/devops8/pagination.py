from rest_framework.pagination import PageNumberPagination


# 重写分页类，默认page_size为5，当小于0时，显示所有数据
class Pagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

    def get_page_size(self, request):
            page_size = int(request.query_params.get('page_size', 5))
            if page_size > 0:
                return page_size
            else:
                pass