from fastapi import APIRouter

from services.profile_builder import ProfileBuilder
from services.risk_engine import RiskEngine

router = APIRouter()

profile_builder = ProfileBuilder()
risk_engine = RiskEngine()


@router.get("/audit/{entity_id}")
def generate_audit(entity_id: str):

    profiles = profile_builder.build_profiles()

    for profile in profiles:

        if profile["entity_id"] == entity_id:

            risk = risk_engine.calculate_risk(
                profile,
                vehicles=[
                    {
                        "vehicle_type": "Prado",
                        "engine_cc": 3000
                    }
                ],
                utility_bill=120000
            )

            risk_level = "Low"

            if risk["risk_score"] >= 75:
                risk_level = "Critical"
            elif risk["risk_score"] >= 50:
                risk_level = "High"
            elif risk["risk_score"] >= 25:
                risk_level = "Medium"

            estimated_leakage = (
                risk["risk_score"] * 50000
            )

            return {
                "entity_id": entity_id,
                "citizen": profile["master_name"],

                "risk_score": risk["risk_score"],
                "risk_level": risk_level,

                "declared_income":
                    profile["declared_income"],

                "filer_status":
                    profile["filer_status"],

                "summary":
                    f"{profile['master_name']} shows indicators of possible tax under-reporting.",

                "findings":
                    risk["reasons"],

                "estimated_leakage":
                    estimated_leakage,

                "recommendation":
                    (
                        "Priority Audit"
                        if risk["risk_score"] >= 75
                        else "Detailed Review"
                        if risk["risk_score"] >= 50
                        else "Monitor"
                    ),

                "audit_confidence":
                    profile.get(
                        "profile_confidence",
                        90
                    )
            }

    return {
        "error": "Citizen not found"
    }