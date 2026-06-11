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

        graph = nx.Graph()

        profiles = (
            self.profile_builder
            .build_profiles()
        )

        for profile in profiles:

            entity_id = (
                profile["entity_id"]
            )

            enrichment = (
                self.enrichment_service
                .enrich(profile)
            )

            risk = (
                self.risk_engine
                .calculate_risk(
                    profile,
                    vehicles=enrichment[
                        "vehicles"
                    ],
                    utility_bill=enrichment[
                        "max_bill"
                    ]
                )
            )

            # ---------------------
            # CITIZEN NODE
            # ---------------------

            graph.add_node(
                entity_id,
                type="citizen",
                label=profile[
                    "master_name"
                ]
            )

            # ---------------------
            # VEHICLES
            # ---------------------

            for vehicle in enrichment[
                "vehicles"
            ]:

                vehicle_id = (
                    vehicle[
                        "vehicle_id"
                    ]
                )

                graph.add_node(
                    vehicle_id,
                    type="vehicle",
                    label=vehicle[
                        "vehicle_type"
                    ]
                )

                graph.add_edge(
                    entity_id,
                    vehicle_id,
                    relation="OWNS"
                )

            # ---------------------
            # UTILITY BILL
            # ---------------------

            if (
                enrichment["max_bill"]
                > 0
            ):

                utility_node = (
                    f"{entity_id}_UTILITY"
                )

                graph.add_node(
                    utility_node,
                    type="utility",
                    label=
                    f"PKR {enrichment['max_bill']:,}"
                )

                graph.add_edge(
                    entity_id,
                    utility_node,
                    relation="PAYS"
                )

            # ---------------------
            # FILER STATUS
            # ---------------------

            status_node = (
                f"{entity_id}_STATUS"
            )

            graph.add_node(
                status_node,
                type="status",
                label=profile[
                    "filer_status"
                ]
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
                label=
                f"Income: PKR {profile['declared_income']:,}"
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
                label=
                f"Tax: PKR {profile['tax_paid']:,}"
            )

            graph.add_edge(
                entity_id,
                tax_node,
                relation="PAID"
            )

            # ---------------------
            # COMPLIANCE SCORE
            # ---------------------

            score_node = (
                f"{entity_id}_TCDS"
            )

            graph.add_node(
                score_node,
                type="risk",
                label=
                f"TCDS {risk['tax_compliance_deviation_score']}"
            )

            graph.add_edge(
                entity_id,
                score_node,
                relation="FLAGGED"
            )

        return graph