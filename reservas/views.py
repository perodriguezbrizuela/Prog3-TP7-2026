from django.contrib import messages
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from .models import ActividadDeportiva


def agregar_actividad(request):
    """Muestra el formulario y registra una actividad deportiva mediante POST."""
    if request.method == "GET":
        return render(request, "reservas/agregar_actividad.html")

    if request.method != "POST":
        return HttpResponseNotAllowed(["GET", "POST"])

    # Recuperar y limpiar los datos enviados por el formulario.
    datos = {
        "nombre": request.POST.get("nombre", "").strip(),
        "descripcion": request.POST.get("descripcion", "").strip(),
        "lugar": request.POST.get("lugar", "").strip(),
        "cupo": request.POST.get("cupo", "").strip(),
    }
    errores = []

    # Validar los campos de texto.
    for campo in ("nombre", "descripcion", "lugar"):
        if not datos[campo]:
            errores.append(f"El campo {campo} es obligatorio.")

    # Validar que el cupo sea un entero positivo.
    try:
        cupo = int(datos["cupo"])
        if cupo <= 0:
            errores.append("El cupo debe ser mayor que cero.")
    except (TypeError, ValueError):
        cupo = None
        errores.append("El cupo debe ser un número entero válido.")

    if errores:
        for error in errores:
            messages.error(request, error)
        return render(
            request,
            "reservas/agregar_actividad.html",
            {"datos": datos},
        )

    # Guardar el registro mediante el ORM de Django.
    ActividadDeportiva.objects.create(
        nombre=datos["nombre"],
        descripcion=datos["descripcion"],
        lugar=datos["lugar"],
        cupo=cupo,
    )
    messages.success(request, "La actividad deportiva se registró correctamente.")
    return redirect("reservas:lista_actividades")


def lista_actividades(request):
    """Muestra todas las actividades registradas."""
    actividades = ActividadDeportiva.objects.all().order_by("id")
    return render(
        request,
        "reservas/lista_actividades.html",
        {"actividades": actividades},
    )


def detalle_actividad(request, actividad_id):
    """Muestra una actividad; devuelve 404 si el identificador no existe."""
    actividad = get_object_or_404(ActividadDeportiva, pk=actividad_id)
    return render(
        request,
        "reservas/detalle_actividad.html",
        {"actividad": actividad},
    )
