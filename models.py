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

