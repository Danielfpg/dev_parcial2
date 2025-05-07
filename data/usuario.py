from sqlalchemy import Column, Integer, String, Enum, Boolean
from sqlalchemy.orm import relationship
from estados import EstadoUsuario
from utils.connection_db import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    estado = Column(Enum(EstadoUsuario), default=EstadoUsuario.activo)
    premium = Column(Boolean, default=False)

    tareas = relationship("Tarea", back_populates="usuario")


