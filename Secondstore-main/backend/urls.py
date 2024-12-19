from django.urls import path
from backend import views

urlpatterns = [
    path('backendindex/',views.backendindex,name="backendindex"),
    path('creg/',views.creg,name="creg"),
    path('save/',views.save,name="save"),
    path('disp/',views.disp,name="disp"),
    path('adstable/',views.adstable,name="adstable"),
    path('usertable/',views.usertable,name="usertable"),
    path('contacttable/',views.contacttable,name="contacttable"),
    path('ceditpage/<int:sid>/',views.ceditpage,name="ceditpage"),
    path('categdel/<int:sid>/', views.categdel, name="categdel"),
    path('ceditsave/<int:sid>/', views.ceditsave, name="ceditsave"),
]