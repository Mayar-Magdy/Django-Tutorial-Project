from django.contrib.auth.models import User , Group
from rest_framework import viewsets , permissions , status
from rest_framework.response import Response
from rest_framework.views import APIView

from tutorial.quickstart.serializers import UserSerializer ,UserCreateSerializer, GroupSerializer, GroupCreateUpdateSerializer

from tutorial.quickstart.permissions import IsOwnerOrAdmin
# selectors
from tutorial.quickstart.selectors import list_users , get_user_by_id , list_groups
# services
from tutorial.quickstart.services import create_user , create_group, update_group, delete_group
# celery
# from .tasks import add 


# Get method using selectors and Post using services for user
class UserViewSet_one(viewsets.ViewSet):
        # permission_classes = [permissions.IsAuthenticated ]

        def get_permissions(self):
   
        #  (create/sign-up)
         if self.action == 'create':
            permission_classes = [permissions.AllowAny]
         else:
            permission_classes = [permissions.IsAuthenticated]
        
         return [permission() for permission in permission_classes]


        def list(self, request):
           users = list_users()
           serializer = UserSerializer(users, many=True, context={'request': request})
           return Response(serializer.data)

        def retrieve(self , request , pk=None):

         try :
            user = get_user_by_id(user_id=pk)
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
         except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        def create(self , request):
            serializer = UserCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            create_user(**serializer.validated_data)
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)





class UserViewSet_Mix(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    # override 
    def perform_create(self, serializer):
        create_user(**serializer.validated_data)


#  API endpoint that allows users to be viewed or edited.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    # serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated , IsOwnerOrAdmin]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    

#   API endpoint that allows groups to be viewed or edited.
class GroupViewSet(viewsets.ModelViewSet):

    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated ]
    

# Get method using selectors and Post using services for group
class GroupViewSet_One(viewsets.ModelViewSet):
  
    queryset = list_groups() 
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated] # maybe IsAdminUser

    def get_serializer_class(self):    
        if self.action in ['create', 'update', 'partial_update']:
            return GroupCreateUpdateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        create_group(**serializer.validated_data)

    def perform_update(self, serializer):
        update_group(group=serializer.instance, **serializer.validated_data)

    def perform_destroy(self, instance):
        delete_group(group=instance)




