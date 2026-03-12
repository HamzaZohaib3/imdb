from rest_framework import serializers
from .models import *


class watchlistserializer(serializers.ModelSerializer):
    class Meta:
        model = watchlist
        fields = '__all__'
    
# class watchlistserializer(serializers.Serializer):
    
#     id = serializers.IntegerField(read_only = True)
#     title = serializers.CharField(max_length=50)
#     story_line = serializers.CharField(max_length=100)
#     # plateform = serializers.ForeignKey("streamplatform", on_delete=models.CASCADE)
#     active = serializers.BooleanField(default=True)
#     created = serializers.DateTimeField(read_only = True)
    
#     def create(self, validated_data):
#         return watchlist.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):

#         instance.title = validated_data.get("title", instance.title)
#         instance.story_line = validated_data.get("story_line", instance.story_line)
#         instance.active = validated_data.get("active", instance.active)
#         instance.created = validated_data.get("created", instance.created)
#         instance.save()
#         return instance
    

class streamplatformserializer(serializers.ModelSerializer):
    watch_list = serializers.StringRelatedField(many=True)
    class Meta:
        model = streamplatform
        fields = '__all__'

# class streamplatformserializer(serializers.Serializer):
    
#     id = serializers.IntegerField(read_only = True)
#     name = serializers.CharField(max_length=50)
#     about = serializers.CharField(max_length=100)
#     website = serializers.URLField(max_length=200)
    
#     def create(self, validated_data):
#         return streamplatform.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):

#         instance.name = validated_data.get("name", instance.name)
#         instance.about = validated_data.get("about", instance.about)
#         instance.website = validated_data.get("website", instance.website)
#         instance.save()
#         return instance