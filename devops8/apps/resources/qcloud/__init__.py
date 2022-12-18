from django.conf import settings
from tencentcloud.common import credential


def getCredential():
    # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey
    return credential.Credential(settings.QCLOUD_SECRETID, settings.QCLOUD_SECRETKEY)

