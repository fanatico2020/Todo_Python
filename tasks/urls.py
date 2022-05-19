"""todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views
urlpatterns = [
    path('helloworld/', views.helloworld),
    path('',views.tasklist,name='task-list'),
    path('task/<int:id>',views.taskview,name='task-view'),
    path('yourname/<str:name>',views.yourname,name='your-name'),
    path('newtask/',views.newtask,name='new-task'),
    path('edittask/<int:id>',views.edittask,name='edit-task'),
    path('deletetask/<int:id>',views.deletetask,name='delete-task'),
    path('changestatus/<int:id>',views.changestatus,name='change-status'),

]
