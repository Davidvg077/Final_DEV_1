from __future__ import annotations

import dataclasses
import datetime
from typing import Optional, List, Dict, ClassVar


@dataclasses.dataclass
class Jugador:
    """Manejamos los atributos de jugador"""

    _id_counter: ClassVar[int] = 0

    id: int = 0
    nombre_completo: str = ""
    numero_camiseta: int = 0
    fecha_nacimiento: Optional[datetime.date] = None
    nacionalidad: str = ""
    foto_ruta: Optional[str] = None
   

    def __post_init__(self) -> None:
        if not isinstance(self.id, int) or self.id <= 0:
            Jugador._id_counter += 1
            self.id = Jugador._id_counter

        if not isinstance(self.nombre_completo, str) or not self.nombre_completo.strip():
            raise ValueError("nombre_completo debe ser una cadena no vacía")

        if not isinstance(self.numero_camiseta, int):
            raise TypeError("numero_camiseta debe ser un entero")
        if self.numero_camiseta < 0 or self.numero_camiseta > 99:
            raise ValueError("numero_camiseta debe estar entre 0 y 99 (incluido)")

        if self.fecha_nacimiento is not None:
            if not isinstance(self.fecha_nacimiento, datetime.date):
                raise TypeError("fecha_nacimiento debe ser un objeto datetime.date")
            today = datetime.date.today()
            if self.fecha_nacimiento > today:
                raise ValueError("fecha_nacimiento no puede ser una fecha en el futuro")

        if not isinstance(self.nacionalidad, str):
            raise TypeError("nacionalidad debe ser una cadena")

        if self.foto_ruta is not None and not isinstance(self.foto_ruta, str):
            raise TypeError("foto_ruta debe ser una cadena con la ruta al archivo o None")

    
    """"""
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre_completo": self.nombre_completo,
            "numero_camiseta": self.numero_camiseta,
            "fecha_nacimiento": self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            "nacionalidad": self.nacionalidad,
            "foto_ruta": self.foto_ruta,
        
        }

@dataclasses.dataclass
class EstadisticaJugadorPartido:
    """Estadísticas de un jugador en un partido."""

    jugador_id: int
    fuera_de_lugar: int = 0
    tarjetas_amarillas: int = 0
    tarjetas_rojas: int = 0
    tiros_al_arco: int = 0
    goles: int = 0
    posicion_stats: Optional[Dict[str, object]] = None

    def __post_init__(self) -> None:
        if not isinstance(self.jugador_id, int) or self.jugador_id <= 0:
            raise TypeError("jugador_id debe ser un entero positivo que identifique al jugador")

        for field_name in ("fuera_de_lugar", "tarjetas_amarillas", "tarjetas_rojas", "tiros_al_arco", "goles"):
            val = getattr(self, field_name)
            if not isinstance(val, int) or val < 0:
                raise ValueError(f"{field_name} debe ser un entero >= 0")

        if self.posicion_stats is not None and not isinstance(self.posicion_stats, dict):
            raise TypeError("posicion_stats debe ser un diccionario con estadísticas específicas de la posición")

