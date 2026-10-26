from django.db import models

# Create your models here.
from django.db import models


class ActividadDeportiva(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    lugar = models.CharField(max_length=100)
    cupo = models.IntegerField()

    def str(self):
        return self.nombre


class Horario(models.Model):

    DIAS_SEMANA = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miercoles', 'Miercoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sabado', 'Sabado'),
        ('Domingo', 'Domingo'),
    ]

    actividad = models.ForeignKey(
    ActividadDeportiva,
    on_delete=models.CASCADE,
    related_name='horarios'
    )


    dia = models.CharField(max_length=15, choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f'{self.actividad.nombre} - {self.dia}'


class Inscripcion(models.Model):

    ESTADOS = [
        ('Activa', 'Activa'),
        ('Cancelada', 'Cancelada'),
    ]

    nombre = models.CharField(max_length=100)

    apellido = models.CharField(max_length=100)

    dni = models.CharField(max_length=20, unique=True)

    fecha_inscripcion = models.DateField(auto_now_add=True)

    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default='Activa'
    )

    horario = models.ForeignKey(
    Horario,
    on_delete=models.CASCADE,
    related_name='inscripciones'
    )

    def __str__(self):
        return f'{self.apellido}, {self.nombre} - DNI: {self.dni}'
