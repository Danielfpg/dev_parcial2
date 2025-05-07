# operations/tarea.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from data.tarea import Tarea
from datetime import datetime
from typing import List, Optional


# Crear una tarea
async def db_create_tarea(
    db_session: AsyncSession,
    nombre: str,
    descripcion: Optional[str],
    usuario_id: int,
):
    nueva_tarea = Tarea(
        nombre=nombre,
        descripcion=descripcion,
        usuario_id=usuario_id,
    )
    async with db_session.begin():
        db_session.add(nueva_tarea)
        await db_session.flush()
        tarea_id = nueva_tarea.id
        await db_session.commit()
    return tarea_id


# Obtener una tarea por ID
async def db_get_tarea(db_session: AsyncSession, tarea_id: int):
    query = select(Tarea).where(Tarea.id == tarea_id)
    result = await db_session.execute(query)
    return result.scalars().first()


# Obtener todas las tareas
async def db_get_all_tareas(db_session: AsyncSession):
    result = await db_session.execute(select(Tarea))
    return result.scalars().all()


# Actualizar una tarea (nombre y descripción por ejemplo)
async def db_update_tarea(
    db_session: AsyncSession,
    tarea_id: int,
    nombre: Optional[str] = None,
    descripcion: Optional[str] = None,
):
    # Verificar que la tarea exista primero
    tarea_existente = await db_get_tarea(db_session, tarea_id)
    if not tarea_existente:
        return False  # Tarea no encontrada

    values = {}
    if nombre is not None:
        values["nombre"] = nombre
    if descripcion is not None:
        values["descripcion"] = descripcion

    # Si no hay cambios, no hacer nada
    if not values:
        return False

    # Agregar fecha de modificación si vas a hacer un update
    values["fecha_modificacion"] = datetime.utcnow()

    await db_session.execute(
        update(Tarea).where(Tarea.id == tarea_id).values(**values)
    )
    await db_session.commit()
    return True


# Eliminar una tarea
async def db_delete_tarea(db_session: AsyncSession, tarea_id: int):
    result = await db_session.execute(delete(Tarea).where(Tarea.id == tarea_id))
    await db_session.commit()
    return result.rowcount > 0
