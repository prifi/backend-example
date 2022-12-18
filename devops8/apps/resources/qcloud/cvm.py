import logging
import json
from resources.qcloud import getCredential
from tencentcloud.cvm.v20170312 import cvm_client, models
from resources.serializers import ServerSerializer

logger = logging.getLogger(__name__)
REGIONS = ["ap-beijing"]

def getCvmClient(region):
    credential = getCredential()
    return cvm_client.CvmClient(credential, region)

def getRegionCvmList(region):
    client = getCvmClient(region)
    req = models.DescribeInstancesRequest()
    resp = client.DescribeInstances(req)
    data = json.loads(resp.to_json_string())
    for instance in data["InstanceSet"]:
        saveInstance(instance)


def saveInstance(instance):
    data = {}
    data["cloud"] = "qcloud"
    data["instanceId"] = instance["InstanceId"]
    data["instanceType"] = instance["InstanceType"]
    data["cpu"] = instance["CPU"]
    data["memory"] = instance["Memory"]
    data["instanceName"] = instance["InstanceName"]
    data["createdTime"] = instance["CreatedTime"]
    data["expiredTime"] = instance["ExpiredTime"]
    data["hostname"] = "qcloud-cvm-{}".format(instance["InstanceId"])
    data["innerIps"] = instance["PrivateIpAddresses"]
    data["publicIps"] = instance["PublicIpAddresses"]
    print(data)
    serializer = ServerSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        print("serializer.errors: ", serializer.errors)


def getCvmList():
    for region in REGIONS:
        try:
            getRegionCvmList(region)
        except Exception as e:
            logger.error("获取qcloud {} 下的cvm失败：{}", region, e.args)
