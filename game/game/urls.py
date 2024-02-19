"""
URL configuration for game project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from app.views import Home
from app.views import register
from app.views import Login
from app.views import RegisterServer
from app.views import GamePage_accept
from app.views import GamePage
from app.views import GamePage_sender
from app.views import GamePage_sender_stone
from app.views import GamePage_sender_paper
from app.views import GamePage_sender_sesores
from app.views import GamePage_delete
from app.views import GamePage_delete2
from app.views import get_value

from app.views import Dashboard

from app.views import Demo

from app.views import Emoji

from app.views import FinalRedirect

from app.views import player_reload

from app.views import Emoji_User
from app.views import LogOut





 















 



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home,name="home"),
    path('register/', register,name="register"),
    path('Login/', Login,name="Login"),
    path('GamePage/', GamePage,name="GamePage"),

    path('Dashboard/', Dashboard,name="Dashboard"),

    path('Demo/', Demo,name="Dashboard"),



    path('GamePage_accept/<int:id>/', GamePage_accept,name="GamePage_accept"),

    path('GamePage_sender/<int:id>/', GamePage_sender,name="GamePage_sender"),


    path('registerServer/<int:id>/', RegisterServer,name="registerServer"),
    
 
    path('GamePage_sender_stone/<str:value>/<int:id>/', GamePage_sender_stone, name="GamePage_sender_stone"),
    path('GamePage_sender_paper/<str:value>/<int:id>/', GamePage_sender_paper, name="GamePage_sender_paper"),
    path('GamePage_sender_sesores/<str:value>/<int:id>/', GamePage_sender_sesores, name="GamePage_sender_sesores"),
    path('Emoji/<str:value>/<int:id>/', Emoji, name="Emoji"),
    path('Emoji_User/<str:value>/<int:id>/', Emoji_User, name="Emoji_User"),

    

    path('GamePage_delete/<int:id>/', GamePage_delete, name="GamePage_delete"),
    path('GamePage_delete2/<int:id>/', GamePage_delete2, name='GamePage_delete2'),
    path('get_value/', get_value, name='get_value'),
    path('LogOut/', LogOut, name='LogOut'),


    
    path('player_reload/', player_reload, name='player_reload'),


    path('FinalRedirect/', FinalRedirect, name='FinalRedirect'),


    





    



]
