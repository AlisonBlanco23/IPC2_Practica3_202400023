from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('producto/<int:id_producto>/', views.detalle_producto, name='detalle_producto'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('editar/<int:id_producto>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:id_producto>/', views.eliminar_producto, name='eliminar_producto'),
]