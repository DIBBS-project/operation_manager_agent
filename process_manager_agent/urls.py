from django.conf.urls import include, url
from django.contrib import admin
from pmaapp import views
from rest_framework.routers import DefaultRouter
import rest_framework.authtoken.views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'ops', views.OpViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),

    url(r'^admin/', include(admin.site.urls)),

]


# Allows to get a token by sending credentials
urlpatterns += [
    url(r'^api-token-auth/', rest_framework.authtoken.views.obtain_auth_token)
]
