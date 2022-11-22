import uuid
from datetime import datetime
from pathlib import Path

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.transaction import atomic
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.decorators import action, api_view, permission_classes

from p43t01 import settings
from .serializers import Organization, OrgSerializer, Host, HostSerizlizer

# 组织树
class OrgViewSet(ModelViewSet):
    queryset = Organization.objects.filter(is_delete=False)
    serializer_class = OrgSerializer
    permission_classes = [] # 先移除权限

    @action(detail=False)
    def tree(self, request):
        """实现节点树层级展示"""
        querset = self.filter_queryset(self.get_queryset())
        results = []
        nodemap = {}
        for o in querset:
            pid = o.parent_id
            id = o.id
            data = self.get_serializer(o).data
            data.setdefault('children', [])
            nodemap[id] = data
            if pid:
                nodemap[pid]['children'].append(data)
            else:
                results.append(data)
        return Response({'results': results})

    def destroy(self, request, *args, **kwargs):
        """重写删除方法，实现逻辑删除"""
        pk = None if self.kwargs.get('pk') == 'null' else self.kwargs['pk']
        targets = []
        if pk:
            targets.append(pk)
        pids = [pk]

        while pids:
            if pids[0] is None:
                cids = self.get_queryset().filter(parent=None).values_list('id', flat=True)
            else:
                cids = self.get_queryset().filter(parent__in=pids).values_list('id', flat=True)
            targets.extend(cids)
            pids = cids  # 递归查子分组ids

        print(targets, '!!!')  # 所有要删除的ids，不包含null
        with atomic(): # 原子性，事务
            self.get_queryset().filter(pk__in=targets).update(is_delete=True)  # 批量逻辑删除分组
            Host.objects.filter(org__in=targets).update(is_delete=True) # 批量逻辑删除分组主机
        return Response(status=204)


# 主机
class HostViewSet(ModelViewSet):
    queryset = Host.objects.filter(is_delete=False)
    serializer_class = HostSerizlizer
    permission_classes = [] # 先移除权限
    filterset_fields = ['org']

# 文件上传
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @permission_classes([])
def upload(request: Request):
    '''
    print(request.data)  # POST, PUT, PATCH
        <QueryDict: {'file': [<InMemoryUploadedFile: Vagrantfile (application/octet-stream)>]}>
        文件在内存中，需要落地
    '''
    file_field_name = 'file'
    fileobj:InMemoryUploadedFile = request.data[file_field_name]
    # print(type(fileobj), fileobj.name, fileobj)

    # 检测文件大小是否超出限制，抛出异常
    # if fileobj.size > 102400:  # 1Gb
    #     raise HugeFileSize('文件超过配置大小')

    # 以日期为目录格式创建目录，写入文件
    basedir = Path(settings.JUMPSERVER_UPLOAD_BASE)
    parentdir = Path('{:%Y/%m/%d}'.format(datetime.now()))
    filename = Path(uuid.uuid4().hex)
    (basedir / parentdir).mkdir(parents=True, exist_ok=True)
    subdir = parentdir / filename
    # (basedir / subdir).write_bytes(fileobj.read())  # 小文件

    # 大文件分chunk读
    with (basedir / subdir).open('wb') as f:
        for chunk in fileobj.chunks():
            f.write(chunk)

    return Response({'name': fileobj.name, 'url': str(subdir)})
