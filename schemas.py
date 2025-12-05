from __future__ import annotations

from datetime import date
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, validator


class DatosDeportivosSchema(BaseModel):
    altura_cm: float = Field(..., gt=0)
    peso_kg: float = Field(..., gt=0)
    pie_dominante: str
    posicion: str
    activo: bool = True


class JugadorSchema(BaseModel):
    nombre_completo: str
    numero_camiseta: int = Field(..., ge=0, le=99)
    fecha_nacimiento: Optional[date]
    nacionalidad: str
    foto_ruta: Optional[str] = None
    datos_deportivos: Optional[DatosDeportivosSchema] = None

    @validator('nombre_completo')
    def nombre_no_vacio(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('El nombre completo no puede estar vacío')
        return v.strip()

    @validator('fecha_nacimiento')
    def fecha_no_futura(cls, v: Optional[date]) -> Optional[date]:
        if v and v > date.today():
            raise ValueError('La fecha de nacimiento no puede ser en el futuro')
        return v


class EstadisticaJugadorPartidoSchema(BaseModel):
    jugador_id: int = Field(..., gt=0)
    fuera_de_lugar: int = Field(0, ge=0)
    tarjetas_amarillas: int = Field(0, ge=0)
    tarjetas_rojas: int = Field(0, ge=0)
    tiros_al_arco: int = Field(0, ge=0)
    goles: int = Field(0, ge=0)
    posicion_stats: Optional[Dict[str, int]] = None


class PartidoSchema(BaseModel):
    fecha: Optional[date]
    equipo_local: str
    equipo_visitante: str
    sigmotoa_es_local: Optional[bool] = None
    goles_local: int = Field(..., ge=0)
    goles_visitante: int = Field(..., ge=0)
    empate_al_final: bool = False
    fue_tiempo_extra: Optional[bool] = False
    fue_penales: Optional[bool] = False
    penales_resultado: Optional[Dict[str, int]] = None
    estadisticas_jugadores: List[EstadisticaJugadorPartidoSchema] = []

    @validator('equipo_local', 'equipo_visitante')
    def equipos_no_vacios(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('El nombre del equipo no puede estar vacío')
        return v.strip()

    class Config:
        orm_mode = True