from rest_framework import serializers                                 
from .models import Publish, Author, Book


class PublishSerializer(serializers.ModelSerializer):      
    class Meta: 
        model = Publish                                                  
        fields = "__all__"       


class AuthorSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Author
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book 
        fields = "__all__"

    def to_author_response(self, author_queryset):
        ret = []
        for author in author_queryset:
            ret.append({
                'id': author.id,
                'name': author.name,
                'email': author.email
            })
        return ret

    def to_representation(self, instance):
        publisher_obj = instance.publisher
        authors = self.to_author_response(instance.authors.all())
        ret = super(BookSerializer, self).to_representation(instance)
        ret["publisher"] = {
            "id": publisher_obj.id,
            "name": publisher_obj.name,
            "address": publisher_obj.address,
        },
        ret["authors"] = authors
        return ret



