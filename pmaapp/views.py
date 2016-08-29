from django.shortcuts import render
import django.contrib.auth

from models import Op
from serializers import UserSerializer, OpSerializer

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route
from django.contrib.auth.models import User

from lib.mister_fs import MisterFs
from lib.mister_hadoop import MisterHadoop
import uuid


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        data2 = {}
        for key in request.data:
            data2[key] = request.data[key]
        data2[u'ops'] = []
        serializer = self.get_serializer(data=data2)
        serializer.is_valid(raise_exception=True)

        # Create the object in database
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OpViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Op.objects.all()
    serializer_class = OpSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    # Override to set the user of the request using the credentials provided to perform the request.
    def create(self, request, *args, **kwargs):
        data2 = {}
        for key in request.data:
            data2[key] = request.data[key]
        serializer = self.get_serializer(data=data2)
        serializer.is_valid(raise_exception=True)

        # Save in the database
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @detail_route(methods=['post'])
    def run_op(self, request, pk=None):
        mister_fs = MisterFs()
        op = Op.objects.get(pk=pk)
        print(op)
        username = op.user.username
        tmp_password = str(uuid.uuid4())
        random_file_name = str(uuid.uuid4())
        generated_script = """
#!/bin/bash;
#set -x;
export USER="%s"
export PASSWORD="%s"
%s
touch %s_finished
        """ % (username, tmp_password, op.script, random_file_name)
        mister_fs.create_file(random_file_name, generated_script)
        op.status = "RUNNING"
        op.save()
        print("running op via tmp/%s script" % (random_file_name))
        mister_fs.run_file(random_file_name)
        op.status = "FINISHED"
        op.save()

        # Serializing the Op response
        serializer = self.get_serializer(op)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    @list_route()
    def get_executions(self, request):
        mister_hadoop = MisterHadoop()
        executions = mister_hadoop.get_running_jobs()
        print("executions: %s" % (executions))
        return Response(executions)


