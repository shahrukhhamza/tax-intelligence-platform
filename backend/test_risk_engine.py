from services.risk_engine import (
    RiskEngine
)

engine = RiskEngine()

profile = {
    "declared_income": 350000,
    "filer_status": "Non-Filer"
}

vehicles = [
    {
        "vehicle_type": "Prado",
        "engine_cc": 3000
    }
]

result = engine.calculate_risk(
    profile,
    vehicles=vehicles,
    utility_bill=120000
)

print(result)