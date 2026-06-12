import networkx as nx

from services.profile_builder import ProfileBuilder
from services.data_enrichment import DataEnrichment
from services.risk_engine import RiskEngine


class GraphBuilder:

    def __init__(self):

        self.profile_builder = ProfileBuilder()

        self.enrichment_service = (
            DataEnrichment()
        )

        self.risk_engine = (
            RiskEngine()
        )

    def build_graph(self):

        print("🔥 NEW GRAPH BUILDER LOADED 🔥")

        graph = nx.Graph()

        profiles = (
            self.profile_builder
            .build_profiles()
        )

        for profile in profiles:

            entity_id = profile["entity_id"]

            enrichment = (
                self.enrichment_service
                .enrich(profile)
            )

            risk = (
                self.risk_engine
                .calculate_risk(
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

            print("\n====================")
            print("PROFILE:", profile["master_name"])
            print("ENTITY:", entity_id)
            print("MAX BILL:", enrichment["max_bill"])
            print("VEHICLES:", len(enrichment["vehicles"]))
            print("PROPERTIES:", len(
                enrichment.get(
                    "properties",
                    []
                )
            ))
            print("TAX PAID:", profile.get("tax_paid"))
            print("RISK:", risk)
            print("====================\n")

            # ---------------------
            # CITIZEN NODE
            # ---------------------

            graph.add_node(
                entity_id,
                type="citizen",
                label=profile["master_name"]
            )

            # ---------------------
            # TAX COMPLIANCE SCORE
            # ---------------------

            compliance_node = (
                f"{entity_id}_COMPLIANCE"
            )

            graph.add_node(
                compliance_node,
                type="compliance",
                label=(
                    "TCDS "
                    f"{risk['tax_compliance_deviation_score']}/100"
                )
            )

            graph.add_edge(
                entity_id,
                compliance_node,
                relation="SCORED"
            )

            # ---------------------
            # RISK NODE
            # ---------------------

            risk_node = (
                f"{entity_id}_RISK"
            )

            graph.add_node(
                risk_node,
                type="risk",
                label=(
                    f"{risk['risk_level']} Risk"
                )
            )

            graph.add_edge(
                entity_id,
                risk_node,
                relation="FLAGGED"
            )

            # ---------------------
            # VEHICLE SUMMARY
            # ---------------------

            vehicle_node = (
                f"{entity_id}_VEHICLES"
            )

            graph.add_node(
                vehicle_node,
                type="vehicle_summary",
                label=(
                    f"Vehicles: "
                    f"{enrichment['vehicle_count']}"
                )
            )

            graph.add_edge(
                entity_id,
                vehicle_node,
                relation="OWNS"
            )

            # ---------------------
            # LUXURY VEHICLES
            # ---------------------

            luxury_node = (
                f"{entity_id}_LUXURY"
            )

            graph.add_node(
                luxury_node,
                type="luxury",
                label=(
                    f"Luxury: "
                    f"{enrichment['luxury_vehicle_count']}"
                )
            )

            graph.add_edge(
                vehicle_node,
                luxury_node,
                relation="CONTAINS"
            )

            # ---------------------
            # PROPERTY NODE
            # ---------------------

            property_count = len(
                enrichment.get(
                    "properties",
                    []
                )
            )

            property_node = (
                f"{entity_id}_PROPERTY"
            )

            graph.add_node(
                property_node,
                type="property",
                label=(
                    f"Properties: "
                    f"{property_count}"
                )
            )

            graph.add_edge(
                entity_id,
                property_node,
                relation="OWNS"
            )

            # ---------------------
            # UTILITY NODE
            # ---------------------

            if enrichment["max_bill"] > 0:

                utility_node = (
                    f"{entity_id}_UTILITY"
                )

                graph.add_node(
                    utility_node,
                    type="utility",
                    label=(
                        f"Bill: PKR "
                        f"{enrichment['max_bill']:,}"
                    )
                )

                graph.add_edge(
                    entity_id,
                    utility_node,
                    relation="PAYS"
                )

            # ---------------------
            # STATUS NODE
            # ---------------------

            status_node = (
                f"{entity_id}_STATUS"
            )

            graph.add_node(
                status_node,
                type="status",
                label=profile["filer_status"]
            )

            graph.add_edge(
                entity_id,
                status_node,
                relation="STATUS"
            )

            # ---------------------
            # INCOME NODE
            # ---------------------

            income_node = (
                f"{entity_id}_INCOME"
            )

            graph.add_node(
                income_node,
                type="income",
                label=(
                    f"Income: PKR "
                    f"{profile['declared_income']:,}"
                )
            )

            graph.add_edge(
                entity_id,
                income_node,
                relation="DECLARES"
            )

            # ---------------------
            # TAX NODE
            # ---------------------

            tax_node = (
                f"{entity_id}_TAX"
            )

            graph.add_node(
                tax_node,
                type="tax",
                label=(
                    f"Tax: PKR "
                    f"{profile.get('tax_paid', 0):,}"
                )
            )

            graph.add_edge(
                entity_id,
                tax_node,
                relation="PAID"
            )

        print(
            f"TOTAL NODES: {len(graph.nodes())}"
        )

        print(
            f"TOTAL EDGES: {len(graph.edges())}"
        )

        return graph