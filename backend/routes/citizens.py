from fastapi import APIRouter

from services.profile_builder import ProfileBuilder
from services.risk_engine import RiskEngine
from services.data_enrichment import DataEnrichment

router = APIRouter()

profile_builder = ProfileBuilder()
risk_engine = RiskEngine()
enrichment_service = DataEnrichment()


@router.get("/live-citizens")
def get_live_citizens():

    profiles = profile_builder.build_profiles()

    results = []

    for profile in profiles:

        enrichment = (
            enrichment_service.enrich(
                profile
            )
        )

        risk = risk_engine.calculate_risk(
            profile,
            vehicles=enrichment.get(
                "vehicles",
                []
            ),
            utility_bill=enrichment.get(
                "max_bill",
                0
            ),
            properties=enrichment.get(
                "properties",
                []
            )
        )

        results.append({

            "entity_id":
            profile["entity_id"],

            "name":
            profile["master_name"],

            "risk_score":
            risk["risk_score"],

            "risk_level":
            risk["risk_level"],

            "vehicle_count":
            enrichment["vehicle_count"],

            "property_count":
            enrichment["property_count"],

            "max_utility_bill":
            enrichment["max_bill"]

        })

    results.sort(
        key=lambda x: x["risk_score"],
        reverse=True
    )

    return results


@router.get("/live-citizen/{entity_id}")
def get_live_citizen(entity_id: str):

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
                vehicles=enrichment.get(
                    "vehicles",
                    []
                ),
                utility_bill=enrichment.get(
                    "max_bill",
                    0
                ),
                properties=enrichment.get(
                    "properties",
                    []
                )
            )

            return {

                "entity_id":
                profile["entity_id"],

                "name":
                profile["master_name"],

                "aliases":
                profile["aliases"],

                "linked_records":
                profile["linked_records"],

                "declared_income":
                profile["declared_income"],

                "filer_status":
                profile["filer_status"],

                "risk_score":
                risk["risk_score"],

                "risk_level":
                risk["risk_level"],

                "reasons":
                risk["reasons"],

                "vehicle_count":
                enrichment["vehicle_count"],

                "property_count":
                enrichment["property_count"],

                "luxury_vehicle_count":
                enrichment["luxury_vehicle_count"],

                "max_utility_bill":
                enrichment["max_bill"],

                "vehicles":
                enrichment["vehicles"],

                "properties":
                enrichment["properties"]

            }

    return {
        "error": "Citizen not found"
    }