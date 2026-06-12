import pandas as pd
import networkx as nx

from services.entity_resolution import EntityResolver


class ProfileBuilder:

    def __init__(self):

        self.resolver = EntityResolver()

        self.tax_df = pd.read_csv(
            "../data/tax_records.csv"
        )

        # -----------------------------
        # CACHE
        # -----------------------------

        self._cached_profiles = None

    def build_profiles(self):

        # -----------------------------
        # RETURN CACHE
        # -----------------------------

        if self._cached_profiles is not None:

            return self._cached_profiles

        records = self.tax_df.to_dict(
            orient="records"
        )

        record_lookup = {

            record["citizen_id"]: record

            for record in records

        }

        graph = nx.Graph()

        for record in records:

            graph.add_node(
                record["citizen_id"],
                data=record
            )

        total_records = len(records)

        for i in range(total_records):

            record_a = records[i]

            for j in range(
                i + 1,
                total_records
            ):

                record_b = records[j]

                score = (
                    self.resolver
                    .calculate_combined_score(
                        record_a["name"],
                        record_b["name"],
                        record_a["address"],
                        record_b["address"]
                    )
                )

                if score >= 95:

                    graph.add_edge(

                        record_a["citizen_id"],

                        record_b["citizen_id"],

                        score=score

                    )

        profiles = []

        components = list(
            nx.connected_components(
                graph
            )
        )

        for idx, component in enumerate(
            components,
            start=1
        ):

            aliases = set()

            linked_ids = []

            incomes = []

            taxes_paid = []

            filer_statuses = []

            component_records = []

            for citizen_id in component:

                record = record_lookup[
                    citizen_id
                ]

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

                "declared_income":
                max(incomes),

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

        # -----------------------------
        # SAVE CACHE
        # -----------------------------

        self._cached_profiles = profiles

        return profiles