import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

API_BASE = 'http://127.0.0.1:5000/productos'

def lista_productos(request):
    try:
        resp = requests.get(API_BASE, timeout=5)
        resp.raise_for_status()
        productos = resp.json()
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error al conectar con la API: {e}")
        productos = []
    return render(request, 'lista.html', {'productos': productos})

def detalle_producto(request, id_producto):
    try:
        resp = requests.get(f'{API_BASE}/{id_producto}', timeout=5)
        resp.raise_for_status()
        producto = resp.json()
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error al cargar el producto: {e}")
        return redirect('lista_productos')
    return render(request, 'detalle.html', {'producto': producto})

def crear_producto(request):
    if request.method == 'POST':
        payload = {
            'nombre': request.POST.get('nombre', '').strip(),
            'categoria': request.POST.get('categoria', '').strip(),
            'descripcion': request.POST.get('descripcion', '').strip(),
            'precio': request.POST.get('precio', '').strip(),
            'cantidad': request.POST.get('cantidad', '').strip(),
            'fecha_vencimiento': request.POST.get('fecha_vencimiento') or None
        }
        try:
            resp = requests.post(API_BASE, json=payload, timeout=5)
            if resp.status_code == 201:
                messages.success(request, 'Producto creado exitosamente.')
                return redirect('lista_productos')
            else:
                error = resp.json().get('error', 'Error desconocido')
                messages.error(request, f'Error al crear: {error}')
        except requests.exceptions.RequestException as e:
            messages.error(request, f'Error de conexión: {e}')
    return render(request, 'crear.html')

def editar_producto(request, id_producto):
    try:
        resp = requests.get(f'{API_BASE}/{id_producto}', timeout=5)
        resp.raise_for_status()
        producto = resp.json()
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error al cargar el producto: {e}")
        return redirect('lista_productos')

    if request.method == 'POST':
        payload = {
            'nombre': request.POST.get('nombre', '').strip(),
            'categoria': request.POST.get('categoria', '').strip(),
            'descripcion': request.POST.get('descripcion', '').strip(),
            'precio': request.POST.get('precio', '').strip(),
            'cantidad': request.POST.get('cantidad', '').strip(),
            'fecha_vencimiento': request.POST.get('fecha_vencimiento') or None
        }
        try:
            resp = requests.put(f'{API_BASE}/{id_producto}', json=payload, timeout=5)
            if resp.status_code == 200:
                messages.success(request, 'Producto actualizado.')
                return redirect('detalle_producto', id_producto=id_producto)
            else:
                error = resp.json().get('error', 'Error desconocido')
                messages.error(request, f'Error al actualizar: {error}')
        except requests.exceptions.RequestException as e:
            messages.error(request, f'Error de conexión: {e}')
    return render(request, 'editar.html', {'producto': producto})

def eliminar_producto(request, id_producto):
    try:
        resp = requests.delete(f'{API_BASE}/{id_producto}', timeout=5)
        if resp.status_code == 200:
            messages.success(request, 'Producto eliminado.')
        else:
            error = resp.json().get('error', 'Error desconocido')
            messages.error(request, f'Error al eliminar: {error}')
    except requests.exceptions.RequestException as e:
        messages.error(request, f'Error de conexión: {e}')
    return redirect('lista_productos')