from django.urls import path

from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, PostSearch, BaseRegisterView, IndexView, \
    CategoryListView, subscribe, upgrade_me, ReplyList
from django.contrib.auth.views import LoginView, LogoutView
from billboard import views

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),
    path('index/', IndexView.as_view(), name='index'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('categories/<int:pk>/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('update_reply_status/<int:pk>/<slug:type>', views.update_reply_status, name='update_reply_status'),
    path('replies/', ReplyList.as_view(), name='replies'),
]
