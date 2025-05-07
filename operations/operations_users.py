from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from data.usuario import Usuario
from data.estados import EstadoUsuario

# Crear un usuario
async def db_create_usuario(db_session: AsyncSession, nombre: str, email: str):
    nuevo_usuario = Usuario(nombre=nombre, email=email)
    db_session.add(nuevo_usuario)
    await db_session.commit()
    await db_session.refresh(nuevo_usuario)
    return nuevo_usuario

# Consultar todos los usuarios
async def db_get_all_usuarios(db_session: AsyncSession):
    result = await db_session.execute(select(Usuario))
    return result.scalars().all()

# Consultar un usuario por ID

async def db_get_usuario(db_session, usuario_id: int):
    result = await db_session.execute(select(Usuario).where(Usuario.id == usuario_id))
    return result.scalars().first()

# Actualizar estado del usuario
async def db_update_estado_usuario(db_session: AsyncSession, usuario_id: int, nuevo_estado: EstadoUsuario):

    usuario_existente = await db_get_usuario(db_session, usuario_id)
    if not usuario_existente:
        return False

    query = (
        update(Usuario)
        .where(Usuario.id == usuario_id)
        .values(estado=nuevo_estado)
    )
    result = await db_session.execute(query)
    await db_session.commit()
    return result.rowcount > 0

# Hacer usuario premium
async def db_update_premium_usuario(db_session: AsyncSession, usuario_id: int, es_premium: bool):

    usuario_existente = await db_get_usuario(db_session, usuario_id)
    if usuario_existente.premium == es_premium:
        return False

    result = await db_session.execute(
        update(Usuario)
        .where(Usuario.id == usuario_id)
        .values(premium=es_premium)
    )
    await db_session.commit()
    return result.rowcount > 0

# Filtrar usuarios por estado
async def db_get_usuarios_por_estado(db_session: AsyncSession, estado: EstadoUsuario):
    result = await db_session.execute(
        select(Usuario).where(Usuario.estado == estado)
    )
    return result.scalars().all()

# Filtrar usuarios Premium y Activo
async def db_get_usuarios_premium_activo(db_session: AsyncSession):
    result = await db_session.execute(
        select(Usuario).where(
            Usuario.premium == True,
            Usuario.estado == EstadoUsuario.activo
        )
    )
    return result.scalars().all()
