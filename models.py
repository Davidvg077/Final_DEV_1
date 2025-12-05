from __future__ import annotations
import dataclasses
import datetime
from typing import Optional, List, Dict, ClassVar


@dataclasses.dataclass
class DatosDeportivos:
    
    altura_cm: float = 0.0
    peso_kg: float = 0.0
    pie_dominante: str = "Derecho"
    posicion: str = ""
    activo: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.altura_cm, (int, float)):
            raise TypeError("altura_cm debe ser numérico (cm)")
        if self.altura_cm <= 0:
            raise ValueError("altura_cm debe ser mayor que 0")

        if not isinstance(self.peso_kg, (int, float)):
            raise TypeError("peso_kg debe ser numérico (kg)")
        if self.peso_kg <= 0:
            raise ValueError("peso_kg debe ser mayor que 0")

        valid_pies = {"derecho", "izquierdo", "ambidiestro"}
        if not isinstance(self.pie_dominante, str):
            raise TypeError("pie_dominante debe ser una cadena")
        pd_norm = self.pie_dominante.strip().lower()
        if pd_norm not in valid_pies:
            raise ValueError("pie_dominante debe ser 'Derecho', 'Izquierdo' o 'Ambidiestro'")
        self.pie_dominante = pd_norm.capitalize()

        if not isinstance(self.posicion, str):
            raise TypeError("posicion debe ser una cadena")
        if not self.posicion.strip():
            raise ValueError("posicion no puede estar vacía")

        if not isinstance(self.activo, bool):
            raise TypeError("activo debe ser un booleano")


@dataclasses.dataclass
class Jugador:
    """Modelo simple para representar un jugador con id autonumérico."""

    _id_counter: ClassVar[int] = 0

    id: int = 0
    nombre_completo: str = ""
    numero_camiseta: int = 0
    fecha_nacimiento: Optional[datetime.date] = None
    nacionalidad: str = ""
    foto_ruta: Optional[str] = None
    datos_deportivos: Optional[DatosDeportivos] = None

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

        if self.datos_deportivos is not None and not isinstance(self.datos_deportivos, DatosDeportivos):
            raise TypeError("datos_deportivos debe ser un objeto DatosDeportivos o None")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre_completo": self.nombre_completo,
            "numero_camiseta": self.numero_camiseta,
            "fecha_nacimiento": self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            "nacionalidad": self.nacionalidad,
            "foto_ruta": self.foto_ruta,
            "datos_deportivos": dataclasses.asdict(self.datos_deportivos) if self.datos_deportivos else None,
        }


@dataclasses.dataclass
class EstadisticaJugadorPartido:
    

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


@dataclasses.dataclass
class Partido:
    

    _id_counter: ClassVar[int] = 0

    id: int = 0
    fecha: Optional[datetime.date] = None
    equipo_local: str = ""
    equipo_visitante: str = ""
    sigmotoa_es_local: Optional[bool] = None
    goles_local: int = 0
    goles_visitante: int = 0
    empate_al_final: bool = False
    fue_tiempo_extra: Optional[bool] = None
    fue_penales: Optional[bool] = None
    penales_resultado: Optional[Dict[str, int]] = None
    estadisticas_jugadores: List[EstadisticaJugadorPartido] = dataclasses.field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.id, int) or self.id <= 0:
            Partido._id_counter += 1
            self.id = Partido._id_counter

        if self.fecha is not None and not isinstance(self.fecha, datetime.date):
            raise TypeError("fecha debe ser datetime.date o None")

        for g_field in ("goles_local", "goles_visitante"):
            g = getattr(self, g_field)
            if not isinstance(g, int) or g < 0:
                raise ValueError(f"{g_field} debe ser un entero >= 0")

        if self.penales_resultado is not None:
            if not isinstance(self.penales_resultado, dict):
                raise TypeError("penales_resultado debe ser un diccionario con los goles de penales")
            for k, v in self.penales_resultado.items():
                if not isinstance(v, int) or v < 0:
                    raise ValueError("los valores en penales_resultado deben ser enteros >= 0")

        if not isinstance(self.estadisticas_jugadores, list):
            raise TypeError("estadisticas_jugadores debe ser una lista")
        for ej in self.estadisticas_jugadores:
            if not isinstance(ej, EstadisticaJugadorPartido):
                raise TypeError("cada elemento en estadisticas_jugadores debe ser EstadisticaJugadorPartido")

    def resultado_para_sigmotoa(self) -> Optional[str]:
        if self.sigmotoa_es_local is None:
            return None
        goles_sigm = self.goles_local if self.sigmotoa_es_local else self.goles_visitante
        goles_opp = self.goles_visitante if self.sigmotoa_es_local else self.goles_local
        if goles_sigm > goles_opp:
            return "GANO"
        if goles_sigm < goles_opp:
            return "PERDIO"
        return "EMPATO"

    def set_penales(self, sigmotoa_penales: int, oponente_penales: int, sigmotoa_key: str = "sigmotoa", oponente_key: str = "oponente") -> None:
        if not (isinstance(sigmotoa_penales, int) and isinstance(oponente_penales, int)):
            raise TypeError("Los resultados de penales deben ser enteros")
        if sigmotoa_penales < 0 or oponente_penales < 0:
            raise ValueError("Los resultados de penales deben ser >= 0")
        self.fue_penales = True
        self.penales_resultado = {sigmotoa_key: sigmotoa_penales, oponente_key: oponente_penales}