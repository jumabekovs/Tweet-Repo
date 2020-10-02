from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
# from .yasg import urlpatterns as dic_url, schema_view
from rest_framework.routers import DefaultRouter

# from tweetapp.views import PostViewSet
# from account.views import ProfileViewSet
# from rest_framework_swagger.views import get_swagger_view
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
schema_view = get_schema_view(title='Blog API')

# API_TITLE = 'Blog API'
# API_DESCRIPTION = 'A Web API for creating and editing blog posts.'
# schema_view = get_swagger_view(title=API_TITLE)

router = DefaultRouter()
router.register('tweets', PostViewSet)
# router.register('comment', CommentViewSet) #поменяли местами пост и твит, коммент # we wont use 'em
# router.register('profile', ProfileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include(router.urls)), # main/tweets/ or main/profile
    path('account/', include('account.urls')), #account/login/ or account/logout
    # path('swagger-docs/', schema_view),
    path('twitter/', include('tweetapp.urls')),
    path('docs/', include_docs_urls(title='Blog API')),
    # path('schema/', schema_view),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += dic_url