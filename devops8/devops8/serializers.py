import logging
from rest_framework import serializers
from resources.models import Server, Cloud, IP

logger = logging.getLogger(__name__)


class ServerSerializer(serializers.Serializer):
    id              = serializers.ReadOnlyField()
    cloud           = serializers.PrimaryKeyRelatedField(queryset=Cloud.objects.all(), many=False)
    instanceId      = serializers.CharField(required=True)
    instanceType    = serializers.CharField(required=True)
    cpu             = serializers.CharField(required=True)
    memory          = serializers.CharField(required=True)
    instanceName    = serializers.CharField(required=True)
    createdTime     = serializers.DateTimeField(required=True, format="%Y-%m-%d %H:%M%S")
    expiredTime     = serializers.DateTimeField(required=True, format="%Y-%m-%d %H:%M%S")
    hostname        = serializers.CharField(required=True)
    publicIps       = serializers.ListField(required=True, write_only=True)
    innerIps        = serializers.ListField(required=True, write_only=True)

    class Meta:
        model = Server
        fields = "__all__"

    def getCloudPk(self, code):
        try:
            obj = Cloud.objects.get(code__exact=code)
            return obj.id
        except Cloud.DoesNotExist:
            logger.error("云厂商不存在: {}".format(code))
            raise serializers.ValidationError("云厂商不存在")
        except Exception as e:
            logger.error("云厂商错误: ".format(e.args))
            raise serializers.ValidationError("云厂商错误")

    def to_internal_value(self, data):
        data["cloud"] = self.getCloudPk(data["cloud"])
        print("to_internal_value: ", data)
        return super(ServerSerializer, self).to_internal_value(data)

    def getInstance(self, instanceId):
        try:
            return Server.objects.get(instanceId__exact=instanceId)
        except Server.DoesNotExist:
            return None
        except Exception as e:
            logger.error("服务器错误: ".format(e.args))
            raise serializers.ValidationError("服务器错误")

    def create(self, validated_data):
        instance = self.getInstance(validated_data["instanceId"])
        if instance is not None:
            return self.update(instance, validated_data)
        innerIps = validated_data.pop("innerIps")
        publicIps = validated_data.pop("publicIps")
        instance = Server.objects.create(**validated_data)
        self.check_inner_ip(instance, innerIps)
        self.check_public_ip(instance, publicIps)
        return instance

    def update(self, instance, validated_data):
        instance.cpu = validated_data.get("cpu", "")
        self.check_inner_ip(instance, validated_data['innerIps'])
        self.check_public_ip(instance, validated_data['publicIps'])
        return instance

    def check_inner_ip(self, instance, innerIps):
        ip_queryset = instance.innerIpAddress.all()
        current_ip_objs = []
        for ip in innerIps:
            try:
                ip_obj = ip_queryset.get(ip__exact=ip)
            except Ip.DoesNotExist:
                ip_obj = Ip.objects.create(ip=ip, inner=instance)
            current_ip_objs.append(ip_obj)
        self.cleanip(ip_queryset, current_ip_objs)

    def check_public_ip(self, instance, publicIps):
        ip_queryset = instance.publicIpAddress.all()
        current_ip_objs = []
        for ip in publicIps:
            try:
                ip_obj = ip_queryset.get(ip__exact=ip)
            except Ip.DoesNotExist:
                ip_obj = Ip.objects.create(ip=ip, public=instance)
            current_ip_objs.append(ip_obj)
        self.cleanip(ip_queryset, current_ip_objs)

    def cleanip(self, ip_queryset, current_ip_objs):
        not_exists_ip = set(ip_queryset) - set(current_ip_objs)
        for obj in not_exists_ip:
            obj.delete()