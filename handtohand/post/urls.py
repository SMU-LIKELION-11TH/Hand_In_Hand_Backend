from django.urls import path
from post import views


urlpatterns = [
    path('area/create/', views.create_area, name='area-create'),
    path('area/<int:pk>/delete/', views.delete_area, name='area-delete'),
    path('create/', views.create_post, name='create_post'),
    path('post/', views.post_list, name='post_list'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('declare_post/<int:pk>/', views.declare_post, name='declare_post'),
    # path('update/<int:id>/', views.update_post, name='update_post'),
    # path('delete/<int:id>/', views.delete_post, name='delete_post'),
    path('delete/<int:pk>/', views.post_delete, name="post_delete"),
    path('update/<int:pk>/', views.update_post, name="update_post"),
    path('my_post/', views.my_post, name="my_post"),
    path('area/', views.get_areas, name="get_areas")

]