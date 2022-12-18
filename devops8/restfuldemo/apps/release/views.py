from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from utils.jenkins_api import JenkinsApi


from .serializers import DeploySerializer
from .models import Deploy
from time import sleep

User = get_user_model()


class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class DeployViewset(viewsets.ModelViewSet):
    """
    create:
    申请上线
    list:
    获取上线列表
    retrieve:
    获取上线信息
    update:
    代码更新信息
    delete:
    取消上线
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated, permissions.DjangoModelPermissions)
    queryset = Deploy.objects.all()
    serializer_class = DeploySerializer
    pagination_class = Pagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('apply_time', 'deploy_time')

    def get_queryset(self):
        rate = self.request.GET.get('status', None)
        applicant = self.request.user
        role = applicant.groups.all().values('name')
        role_name = [r['name'] for r in role]
        queryset = super(DeployViewset, self).get_queryset()

        # 判断传来的status值判断是申请列表还是历史列表
        if rate and int(rate) <= 2:
            queryset = queryset.filter(status__lte=2)
        elif rate and int(rate) > 2:
            queryset = queryset.filter(status__gte=2)
        else:
            pass

        # 判断登陆用户是否是管理员，是则显示所有项目，否则只显示自己的项目
        if "sa" not in role_name:
            queryset = queryset.filter(applicant=applicant)
        return queryset

    def partial_update(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        data = request.data
        data['assign_to'] = request.user
        print(data)
        if int(data['status']) == 3:
            print("1111")
            jenkins = JenkinsApi()
            number = jenkins.get_next_build_number(data['name'])
            jenkins.build_job(data['name'], parameters={'tag': data['version']})
            sleep(30)
            console_output = jenkins.get_build_console_output(data['name'], number)
            data['console_output'] = console_output
        Deploy.objects.filter(pk=pk).update(**data)
        return Response(status=status.HTTP_204_NO_CONTENT)

