from django.contrib.auth.models import User , Group
from rest_framework import viewsets , permissions
from tutorial.quickstart.serializers import UserSerializer ,UserCreateSerializer, GroupSerializer
from tutorial.quickstart.permissions import IsOwnerOrAdmin



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