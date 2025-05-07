import enum

class EstadoTarea(enum.Enum):
    pendiente = "Pendiente"
    en_ejecucion = "En ejecución"
    realizada = "Realizada"
    cancelada = "Cancelada"

class EstadoUsuario(enum.Enum):
    activo = "Activo"
    inactivo = "Inactivo"
    eliminado = "Eliminado"
