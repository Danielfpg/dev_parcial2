from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from utils.connection_db import init_db, get_session
from sqlalchemy.ext.asyncio import AsyncSession
from operations.operations_users import (
    db_create_usuario,
    db_get_usuario,
    db_get_all_usuarios,
    db_update_estado_usuario,
    db_update_premium_usuario,
    db_get_usuarios_por_estado,
    db_get_usuarios_premium_activo,
)
from operations.operations_tasks import (
    db_create_tarea,
    db_get_tarea,
    db_get_all_tareas,
    db_update_tarea,
    db_delete_tarea,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello Profe"}

# ---------- USUARIOS ----------

@app.post("/usuarios")
async def crear_usuario(id: int, nombre: str, email: str, db: AsyncSession = Depends(get_session)):
    return await db_create_usuario(db, id, nombre, email)


@app.get("/usuarios/estado/{estado}")
async def obtener_usuarios_por_estado(estado: str, db: AsyncSession = Depends(get_session)):
    estado_str = estado.strip().lower()
    if estado_str == "activo":
        estado_enum = EstadoUsuario.activo
    elif estado_str == "inactivo":
        estado_enum = EstadoUsuario.inactivo
    elif estado_str == "eliminado":
        estado_enum = EstadoUsuario.eliminado
    else:
        raise HTTPException(status_code=400, detail="Estado inválido")

    return await db_get_usuarios_por_estado(db, estado_enum)

@app.get("/usuarios/{usuario_id}")
async def obtener_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    usuario = await db_get_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

from data.estados import EstadoUsuario

@app.patch("/usuarios/{usuario_id}/estado")
async def actualizar_estado_usuario(usuario_id: int, nuevo_estado: str, db: AsyncSession = Depends(get_session)):
    estado_str = nuevo_estado.strip().lower()
    if estado_str == "activo":
        estado_enum = EstadoUsuario.activo
    elif estado_str == "inactivo":
        estado_enum = EstadoUsuario.inactivo
    elif estado_str == "eliminado":
        estado_enum = EstadoUsuario.eliminado
    else:
        raise HTTPException(status_code=400, detail="Estado inválido")

    actualizado = await db_update_estado_usuario(db, usuario_id, estado_enum)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"mensaje": "Estado actualizado correctamente"}


@app.patch("/usuarios/{usuario_id}/premium")
async def hacer_usuario_premium(usuario_id: int, es_premium: bool, db: AsyncSession = Depends(get_session)):
    return await db_update_premium_usuario(db, usuario_id, es_premium)

@app.get("/usuarios/estado/{estado}")
async def obtener_usuarios_por_estado(estado: str, db: AsyncSession = Depends(get_session)):
    return await db_get_usuarios_por_estado(db, estado)

@app.get("/usuarios/activos-premium")
async def obtener_usuarios_activos_y_premium(db: AsyncSession = Depends(get_session)):
    return await db_get_usuarios_premium_activo(db)

# ---------- TAREAS ----------

@app.post("/tareas")
async def crear_tarea(nombre: str, descripcion: str, usuario_id: int, db: AsyncSession = Depends(get_session)):
    return await db_create_tarea(db, nombre, descripcion, usuario_id)

@app.get("/tareas")
async def obtener_todas_tareas(db: AsyncSession = Depends(get_session)):
    return await db_get_all_tareas(db)

@app.get("/tareas/{tarea_id}")
async def obtener_tarea(tarea_id: int, db: AsyncSession = Depends(get_session)):
    tarea = await db_get_tarea(db, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea

@app.patch("/tareas/{tarea_id}")
async def actualizar_tarea(tarea_id: int, nombre: str = None, descripcion: str = None, db: AsyncSession = Depends(get_session)):
    actualizado = await db_update_tarea(db, tarea_id, nombre, descripcion)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Tarea no encontrada o sin cambios")
    return {"message": "Tarea actualizada"}

@app.delete("/tareas/{tarea_id}")
async def eliminar_tarea(tarea_id: int, db: AsyncSession = Depends(get_session)):
    eliminada = await db_delete_tarea(db, tarea_id)
    if not eliminada:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"message": "Tarea eliminada"}
