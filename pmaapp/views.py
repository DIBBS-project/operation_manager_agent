from django.shortcuts import render
import django.contrib.auth

from models import Op
from serializers import UserSerializer, OpSerializer

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route

from lib.mister_fs import MisterFs
from lib.mister_hadoop import MisterHadoop
import uuid

class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = django.contrib.auth.get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        data2 = {}
        for key in request.data:
            data2[key] = request.data[key]
        data2[u'ops'] = []
        serializer = self.get_serializer(data=data2)
        serializer.is_valid(raise_exception=True)
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
        random_file_name = str(uuid.uuid4())
        generated_script = """
#!/bin/bash;
#set -x;
%s
touch %s_finished
        """ % (op.script, random_file_name)
        mister_fs.create_file(random_file_name, generated_script)
        op.status = "RUNNING"
        op.save()
        print("running op via tmp/%s script" % (random_file_name))
        mister_fs.run_file(random_file_name)
        op.status = "FINISHED"
        op.save()
        return Response({"Hello"})

    @list_route()
    def get_executions(self, request):
        mister_hadoop = MisterHadoop()
        executions = mister_hadoop.get_running_jobs()
        print("executions: %s" % (executions))
        return Response(executions)


