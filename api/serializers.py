from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from drf_writable_nested.serializers import WritableNestedModelSerializer

from users.models import Profile, Skill, Project

class RegistrationSerializer(serializers.ModelSerializer):
    
    username  = serializers.CharField(
                required=True,
                validators=[UniqueValidator(queryset=User.objects.all(), message='Username already exist!')]
                )
    
    email     = serializers.EmailField(
                required=True,
                validators=[UniqueValidator(queryset=User.objects.all(), message='Email already exist!')],
            )

    password  = serializers.CharField(
                required=True,
                style={'input_type': 'password'},
                write_only=True)
    
    password2 = serializers.CharField(
                required=True,
                style={'input_type': 'password'},
                write_only=True)
    
    class Meta:
        model  = User
        fields = ['username', 'email', 'password', 'password2']
        
    def validate(self, obj):
        if obj['password'] != obj['password2']:
            raise serializers.ValidationError({'password':'Password mismatch!'})
        
        return obj
        
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        ) 
        user.set_password(validated_data['password'])
        user.save()
        return user

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['name']
               
# class LikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Like
#         fields = ['like']

class ProjectSerializer(serializers.ModelSerializer):
    # likes = serializers.SerializerMethodField() 
    
    class Meta:
        model = Project
        fields = ['title', 'link']

    # def get_likes(self, obj):
    #     likes = obj.likes.all().count()
    #     return likes
        
class ProfileSerializers(WritableNestedModelSerializer):
    skills   = SkillSerializer(many=True)     
    projects = ProjectSerializer(many=True)   
    # projects = serializers.SerializerMethodField() 

    class Meta:
        model = Profile
        fields = ['id', 'name', 'email', 'intro', 'looking_for', 'bio', 'github', 'linkedin', 'website', 'location', 'skills', 'projects']
    
    # def get_projects(self,obj):
    #     projects = obj.project_set.all()
    #     serailizer = ProjectSerializer(projects, many=True)
    #     return serailizer.data
    
        
        

