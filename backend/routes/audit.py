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

            risk = (
                risk_engine.calculate_risk(
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
            )

            declared_income = profile.get(
                "declared_income",
                0
            )

            estimated_leakage = int(
                declared_income
                * (
                    risk["risk_score"]
                    / 100
                )
                * 0.20
            )

            return {

                "entity_id":
                entity_id,

                "citizen":
                profile["master_name"],

                "tax_compliance_deviation_score":
                risk[
                    "tax_compliance_deviation_score"
                ],

                "risk_score":
                risk["risk_score"],

                "risk_level":
                risk["risk_level"],

                "declared_income":
                declared_income,

                "tax_paid":
                profile.get(
                    "tax_paid",
                    0
                ),

                "filer_status":
                profile.get(
                    "filer_status",
                    "Unknown"
                ),

                "linked_records":
                len(
                    profile.get(
                        "linked_records",
                        []
                    )
                ),

                "aliases":
                profile.get(
                    "aliases",
                    []
                ),

                "vehicle_count":
                enrichment.get(
                    "vehicle_count",
                    0
                ),

                "luxury_vehicle_count":
                enrichment.get(
                    "luxury_vehicle_count",
                    0
                ),

                "property_count":
                len(
                    enrichment.get(
                        "properties",
                        []
                    )
                ),

                "max_utility_bill":
                enrichment.get(
                    "max_bill",
                    0
                ),

                # -------------------------
                # EXECUTIVE SUMMARY
                # -------------------------

                "summary":
                (
                    f"Citizen "
                    f"{profile['master_name']} "
                    f"was flagged with a "
                    f"Tax Compliance Deviation Score "
                    f"of "
                    f"{risk['risk_score']}/100 "
                    f"({risk['risk_level']} Risk). "
                    f"The entity owns "
                    f"{enrichment.get('vehicle_count', 0)} "
                    f"vehicle(s), "
                    f"{len(enrichment.get('properties', []))} "
                    f"property asset(s), "
                    f"has utility consumption "
                    f"up to PKR "
                    f"{enrichment.get('max_bill', 0):,}, "
                    f"and is classified as "
                    f"{profile.get('filer_status', 'Unknown')}. "
                    f"The assessment was generated "
                    f"using linked tax, vehicle, "
                    f"property and utility records."
                ),

                # -------------------------
                # FINDINGS
                # -------------------------

                "findings":
                risk["reasons"],

                # -------------------------
                # ESTIMATED LEAKAGE
                # -------------------------

                "estimated_leakage":
                estimated_leakage,

                # -------------------------
                # RECOMMENDATION
                # -------------------------

                "recommendation":
                (
                    "Priority Audit"
                    if risk["risk_score"] >= 80
                    else
                    "Detailed Review"
                    if risk["risk_score"] >= 60
                    else
                    "Monitor"
                ),

                # -------------------------
                # CONFIDENCE
                # -------------------------

                "audit_confidence":
                profile.get(
                    "profile_confidence",
                    90
                ),

                # -------------------------
                # AUDIT TRAIL
                # -------------------------

                "audit_trail": [

                    {
                        "step": 1,
                        "action":
                        "Entity Resolution",
                        "result":
                        (
                            f"{len(profile.get('linked_records', []))} "
                            f"records merged into "
                            f"{entity_id}"
                        )
                    },

                    {
                        "step": 2,
                        "action":
                        "Data Enrichment",
                        "result":
                        (
                            f"{enrichment.get('vehicle_count', 0)} "
                            f"vehicles, "
                            f"{len(enrichment.get('properties', []))} "
                            f"properties and utility "
                            f"records linked"
                        )
                    },

                    {
                        "step": 3,
                        "action":
                        "Risk Assessment",
                        "result":
                        (
                            f"Tax Compliance "
                            f"Deviation Score = "
                            f"{risk['risk_score']}"
                        )
                    },

                    {
                        "step": 4,
                        "action":
                        "Compliance Evaluation",
                        "result":
                        risk["risk_level"]
                    }
                ],

                # -------------------------
                # EVIDENCE
                # -------------------------

                "evidence": {

                    "vehicle_count":
                    enrichment.get(
                        "vehicle_count",
                        0
                    ),

                    "luxury_vehicle_count":
                    enrichment.get(
                        "luxury_vehicle_count",
                        0
                    ),

                    "property_count":
                    len(
                        enrichment.get(
                            "properties",
                            []
                        )
                    ),

                    "utility_bill":
                    enrichment.get(
                        "max_bill",
                        0
                    ),

                    "linked_records":
                    len(
                        profile.get(
                            "linked_records",
                            []
                        )
                    ),

                    "identity_variations":
                    len(
                        profile.get(
                            "aliases",
                            []
                        )
                    )
                },

                # -------------------------
                # RAW DATA
                # -------------------------

                "vehicles":
                enrichment.get(
                    "vehicles",
                    []
                ),

                "properties":
                enrichment.get(
                    "properties",
                    []
                )
            }

    return {

        "success": False,

        "error":
        "Citizen not found"
    }