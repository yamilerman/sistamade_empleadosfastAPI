# API REST: Interfaz de Programación de Aplicaciones para compartir recursos

from typing import List, Optional
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Inicializamos una variable donde tendrá todas las caracteristicas de una API REST
app = FastAPI()


# Defino el modelo
class Empleado(BaseModel):
    id: Optional[str] = None
    nombre: str
    puesto: Optional[str] = None
    departamento: str


# Simulo una base de datos
empleados_db = []


# CRUD: Read (Lectura) GET ALL: Leeremos todos los empleados que haya en la bd
@app.get("/empleados/", response_model=list[Empleado])  # decoradores
def obtener_empleados():
    return empleados_db


# CRUD: Create (escribir-crear) POST: agregaremos un nuevo recurso a nuestra bd
@app.post("/empleados/", response_model=Empleado)  # decoradores
def crear_empleado(empleado: Empleado):
    empleado.id = str(
        uuid.uuid4()
    )  # usamos uuid para generar un id unico e irrepetible
    empleados_db.append(empleado)
    return empleado


# CRUD: Read (lectura) GET(individual): Leeremos el empleado que coincida con el ID que pidamos
@app.get("/empleados/{empleado_id}", response_model=Empleado)
def obtener_empleado(empleado_id: str):
    empleado = next(
        (empleado for empleado in empleados_db if empleado.id == empleado_id), None
    )  # Con el next devuelve la primer coincidencia del array
    if empleado is None:
        raise HTTPException(
            status_code=404, detail="Empleado no encontrado"
        )  # no ponemos else porque cunado hay un raise se corta el if
    return empleado


# CRUD: Update (actualizar - modificar) PUT (individual): Modificaremos un recurso que coincida con el id que mandemos
@app.put("/empleados/{empleado_id}", response_model=Empleado)
def actualizar_empleado(empleado_id: str, empleado_actualizado: Empleado):
    empleado = next(
        (empleado for empleado in empleados_db if empleado.id == empleado_id), None
    )  # Con el next devuelve la primer coincidencia del array
    if empleado is None:
        raise HTTPException(
            status_code=404, detail="Empleado no encontrado"
        )  # no ponemos else porque cunado hay un raise se corta el if
    empleado_actualizado.id = empleado_id
    index = empleados_db.index(
        empleado
    )  # Buscamos el indice exacto donde está el curso en nuestra lista (BD)
    empleados_db[index] = empleado_actualizado
    return empleado_actualizado


# CRUD: Delete (borrado - baja) DELETE (individual): eliminaremos un recurso que coincida con el id que mandemos
@app.delete("/empleados/{empleado_id}", response_model=Empleado)
def eliminar_empleado(empleado_id: str):
    empleado = next(
        (empleado for empleado in empleados_db if empleado.id), None
    )  # Con el next devuelve la primer coincidencia del array
    if empleado is None:
        raise HTTPException(
            status_code=404, detail="Empleado no encontrado"
        )  # no ponemos else porque cunado hay un raise se corta el if
    empleados_db.remove(empleado)
    return empleado
