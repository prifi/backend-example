from rest_framework.routers import DefaultRouter
from .views import ProjectListView, ProjectVersionsView


project_router = DefaultRouter()
project_router.register(r'list', ProjectListView, base_name="list")
project_router.register(r'tag', ProjectVersionsView, base_name="tag")
