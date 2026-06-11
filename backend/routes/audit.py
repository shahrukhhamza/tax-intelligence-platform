from fastapi import APIRouter

from services.profile_builder import ProfileBuilder
from services.risk_engine import RiskEngine
from services.data_enrichment import DataEnrichment

router = APIRouter()

profile_builder = ProfileBuilder()
risk_engine = RiskEngine()
enrichment_service = DataEnrichment()


@router.get("/audit/{entity_id}")
def generate_audit(entity_id: str):

    profiles = profile_builder.build_profiles()

    for profile in profiles:

        if profile["entity_id"] == entity_id:

            enrichment = (
                enrichment_service.enrich(
                    profile
                )
            )

            risk = risk_engine.calculate_risk(
                profile,
                vehicles=enrichment["vehicles"],
                utility_bill=enrichment["max_bill"]
            )

            estimated_leakage = (
                risk["risk_score"] * 50000
            )

            return {

                "entity_id":
                entity_id,

                "citizen":
                profile["master_name"],

                "risk_score":
                risk["risk_score"],

                "risk_level":
                risk["risk_level"],

                "declared_income":
                profile["declared_income"],

                "filer_status":
                profile["filer_status"],

                "linked_records":
                len(
                    profile["linked_records"]
                ),

                "aliases":
                profile["aliases"],

                "vehicle_count":
                enrichment["vehicle_count"],

                "luxury_vehicle_count":
                enrichment[
                    "luxury_vehicle_count"
                ],

                "max_utility_bill":
                enrichment["max_bill"],

                "summary":
                (
                    f"{profile['master_name']} "
                    f"shows indicators of possible "
                    f"tax under-reporting based on "
                    f"entity resolution, asset ownership, "
                    f"and utility consumption."
                ),

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
                ),

                "vehicles":
                enrichment["vehicles"]
            }

    return {
        "error": "Citizen not found"
    }