from django.urls import path
from . import views


urlpatterns = [
    path('', views.StartingPageView.as_view(), name='starting-page'),       # Redirect to the Homepage
    path('posts', views.AllPostView.as_view(), name='posts-page'),          # Redirect to the All Posts Page
    path('posts/<slug:slug>', views.PostDetailView.as_view(),               # Redirect to the Single Post Page  
         name='post-detail-page'),  
#     path('delete-comment/<str:pk>', views.deleteComment,               # Redirect to the Single Post Page  
#          name='delete-comment'), 
     path('delete-comment/<str:pk>', views.DeleteComment.as_view(),               # Redirect to the Single Post Page  
         name='delete-comment'),
    path("read-later", views.ReadLaterView.as_view(), name="read-later")    # Redirect to the Marked Post Page
]


