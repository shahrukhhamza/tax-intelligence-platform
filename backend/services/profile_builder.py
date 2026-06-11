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

        # Add nodes

        for record in records:

            graph.add_node(
                record["citizen_id"],
                data=record
            )

        # Similarity edges

        for i in range(len(records)):

            for j in range(i + 1, len(records)):

                score = (
                    self.resolver.calculate_combined_score(
                        records[i]["name"],
                        records[j]["name"],
                        records[i]["address"],
                        records[j]["address"]
                    )
                )

                if score >= 85:

                    graph.add_edge(
                        records[i]["citizen_id"],
                        records[j]["citizen_id"],
                        score=score
                    )

        profiles = []

        components = list(
            nx.connected_components(graph)
        )

        for idx, component in enumerate(
            components,
            start=1
        ):

            component_records = []

            aliases = set()

            linked_ids = []

            incomes = []

            filer_status = []

            for citizen_id in component:

                record = next(
                    r
                    for r in records
                    if r["citizen_id"] == citizen_id
                )

                component_records.append(record)

                aliases.add(record["name"])

                linked_ids.append(citizen_id)

                incomes.append(
                    record["declared_income"]
                )

                filer_status.append(
                    record["filer_status"]
                )

            master_record = component_records[0]

            profiles.append({

                "entity_id":
                f"ENT{idx:03}",

                "master_name":
                master_record["name"],

                "aliases":
                list(aliases),

                "linked_records":
                linked_ids,

                "declared_income":
                max(incomes),

                "filer_status":
                (
                    "Non-Filer"
                    if "Non-Filer"
                    in filer_status
                    else "Filer"
                ),

                "profile_confidence":
                92

            })

        return profiles