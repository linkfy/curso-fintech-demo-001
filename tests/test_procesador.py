from decimal import Decimal

import pytest
from pydantic import ValidationError

from transacciones.procesador import Moneda, Transaccion, aplicar_comision

# Fixtures


@pytest.fixture
def transaccion_base() -> Transaccion:
    return Transaccion(monto=Decimal("100.0"), moneda=Moneda.USD)


@pytest.mark.parametrize(
    ("porcentaje", "esperado"),
    [
        (Decimal("0.5"), Decimal("150.0")),
        (Decimal("0.10"), Decimal("110.0")),
        (Decimal("0.0"), Decimal("100.0")),
    ],
)
def test_aplicar_comision_con_porcentajes_validos(
    transaccion_base: Transaccion, porcentaje: Decimal, esperado: Decimal
) -> None:
    assert aplicar_comision(transaccion_base, porcentaje) == esperado


@pytest.mark.parametrize(
    "porcentaje",
    [
        Decimal("-0.1"),
        Decimal("1.1"),
    ],
)
def test_aplicar_comision_porcentajes_invalidos(
    transaccion_base: Transaccion,
    porcentaje: Decimal,
) -> None:
    with pytest.raises(ValueError):
        aplicar_comision(transaccion_base, porcentaje)


def test_transaccion_rechaza_monto_negativo() -> None:
    with pytest.raises(ValidationError):
        Transaccion(monto=Decimal("-50.0"), moneda=Moneda.USD)
