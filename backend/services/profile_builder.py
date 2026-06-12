import pandas as pd
import networkx as nx

from services.entity_resolution import EntityResolver


class ProfileBuilder:

    def __init__(self):

        self.resolver = EntityResolver()

        self.tax_df = pd.read_csv(
            "../data/tax_records.csv"
        )

        self.vehicle_df = pd.read_csv(
            "../data/vehicle_records.csv"
        )

        self.utility_df = pd.read_csv(
            "../data/utility_bills.csv"
        )

    def build_profiles(self):

        records = self.tax_df.to_dict(
            orient="records"
        )

        graph = nx.Graph()

        # -----------------------------
        # ADD NODES
        # -----------------------------

        for record in records:

            graph.add_node(
                record["citizen_id"],
                data=record
            )

        # -----------------------------
        # ENTITY RESOLUTION
        # STRICT MATCHING
        # -----------------------------

        for i in range(len(records)):

            for j in range(i + 1, len(records)):

                score = (
                    self.resolver
                    .calculate_combined_score(
                        records[i]["name"],
                        records[j]["name"],
                        records[i]["address"],
                        records[j]["address"]
                    )
                )

                # STRICTER THRESHOLD

                if score >= 93:

                    graph.add_edge(

                        records[i]["citizen_id"],

                        records[j]["citizen_id"],

                        score=score

                    )

        profiles = []

        components = list(
            nx.connected_components(
                graph
            )
        )

        # -----------------------------
        # BUILD UNIFIED PROFILES
        # -----------------------------

        for idx, component in enumerate(
            components,
            start=1
        ):

            component_records = []

            aliases = set()

            linked_ids = []

            incomes = []

            taxes_paid = []

            filer_statuses = []

            for citizen_id in component:

                record = next(

                    r

                    for r in records

                    if r["citizen_id"]
                    == citizen_id

                )

                component_records.append(
                    record
                )

                aliases.add(
                    record["name"]
                )

                linked_ids.append(
                    citizen_id
                )

                incomes.append(

                    int(
                        record[
                            "declared_income"
                        ]
                    )

                )

                taxes_paid.append(

                    int(
                        record[
                            "tax_paid"
                        ]
                    )

                )

                filer_statuses.append(

                    record[
                        "filer_status"
                    ]

                )

            master_record = (
                component_records[0]
            )

            # -----------------------------
            # PROFILE CONFIDENCE
            # -----------------------------

            profile_confidence = 85

            if len(component) >= 2:

                profile_confidence = 90

            if len(component) >= 3:

                profile_confidence = 95

            profiles.append({

                "entity_id":
                f"ENT{idx:03}",

                "master_name":
                master_record["name"],

                "aliases":
                sorted(
                    list(
                        aliases
                    )
                ),

                "linked_records":
                linked_ids,

                # Use highest declared income

                "declared_income":
                max(incomes),

                # Sum tax records

                "tax_paid":
                sum(taxes_paid),

                "filer_status":
                (
                    "Non-Filer"
                    if "Non-Filer"
                    in filer_statuses
                    else "Filer"
                ),

                "profile_confidence":
                profile_confidence

            })

        profiles.sort(

            key=lambda x:

            len(
                x["linked_records"]
            ),

            reverse=True

        )

        return profiles