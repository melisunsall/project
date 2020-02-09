from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView,LogoutView

app_name ='forum'
urlpatterns = [
    path('',views.UserFormView.as_view(),name='register'),
    path('<int:pk>/',views.DetailView.as_view(), name='detail'),

    path('about',views.AboutView,name='about'),

    path('intern/list',views.InternsView.as_view(),name='interns'),
    path('intern/add/',views.InternCreate.as_view(),name='intern-add'),
    path('intern/<int:pk>',views.InternView.as_view(), name='intern'),
    path('intern/<int:pk>/upload',views.FileFormView.as_view(), name='upload'),
    path('intern/<int:pk>/add_comment',views.AddComent.as_view(), name='add-comment'),
    path('intern/<int:comment_id>/delete', views.DeleteComment.as_view(), name='delete-comment'),
    path('intern/<int:comment_id>/like', views.VoteComment.as_view(), name='vote-comment'),
    path('intern/<int:pk>/edit',views.InternUptade.as_view(),name='intern-update'),
    path('intern/<int:pk>/delete',views.InternDelete.as_view(),name='intern-delete'),
    path('intern/<int:pk>/vote',views.vote,name='vote'),
    path('intern/<int:pk>/accept', views.accept, name='accept'),

    path('login/',views.loginview, name='login'),
    path('departments', views.DepartmentView.as_view(), name='departments'),
    path('search',views.search_view,name='search'),
    path('logout',views.logoutview, name='logout'),
    path('profile/',views.profile,name='profile'),
    path('calendar',views.CalendarView.as_view(),name='calendar'),
    path('calendar/new_event',views.EventFormView.as_view(),name='add-event'),
]


