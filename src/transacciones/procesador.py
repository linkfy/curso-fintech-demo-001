from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Moneda(Enum):
    """Monedas soportadas por el procesador de transacciones"""

    USD = "USD"
    EUR = "EUR"


class Transaccion(BaseModel):
    """
    Representa una transacción financiera válida

    Attributes:
        monto: Cantidad de dinero de la transacción
        moneda: Moneda en la que se expresa la transacción
    """

    model_config = ConfigDict(strict=True)
    monto: Decimal = Field(gt=0)
    moneda: Moneda


def aplicar_comision(transaccion: Transaccion, porcentaje: Decimal) -> Decimal:
    """
    Aplica una comisión porcentual a una transacción

    Args:
        transaccion: Transacción sobre la que se aplicará la comision
        porcentaje: Comisión expresada como tipo Decimal entre 0 y 1

    Returns:
        Monto tras aplicar comisión

    Raises:
        ValueError: Si el porcentaje no está entre 0 y 1
    """
    if not (Decimal("0") <= porcentaje <= Decimal("1")):
        raise ValueError("El procentaje debe estar entre 0 y 1")

    return transaccion.monto * (Decimal("1") + porcentaje)
