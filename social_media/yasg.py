# from django.urls import path
# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
#
# schema_view = get_schema_view(
#     openapi.Info(
#         title='Twitter API Clone',
#         default_version='v1',
#         description='В проекте реализовано:'
#                     'Crud'
#                     'регистрация'
#                     'комментарии'
#                     'работа с картинками'
#                     'пагинация'
#                     'permission'
#                     'поиск'
#                     'фильтрация',
#         license=openapi.License(name='BSD License')
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )
"""
Since we have not been using swagger, we can get rid of it!

"""

# urlpatterns = [
# #    path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
# #    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
# ]

urlpatterns = [
#    path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('twitter/', schema_view.with_ui('twitter', cache_timeout=0), name='schema-twitter-ui'),
#    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]