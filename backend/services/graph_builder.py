import networkx as nx
import pandas as pd

from services.profile_builder import ProfileBuilder


class GraphBuilder:

    def __init__(self):

        self.profile_builder = ProfileBuilder()

        self.vehicle_df = pd.read_csv(
            "../data/vehicle_records.csv"
        )

        self.utility_df = pd.read_csv(
            "../data/utility_bills.csv"
        )

    def build_graph(self):

        graph = nx.Graph()

        profiles = self.profile_builder.build_profiles()

        # Citizen entities

        for profile in profiles:

            graph.add_node(
                profile["entity_id"],
                type="citizen",
                label=profile["master_name"]
            )

        # Vehicles

        for profile in profiles:

            aliases = profile["aliases"]

            for _, vehicle in self.vehicle_df.iterrows():

                if vehicle["owner_name"] in aliases:

                    vehicle_id = vehicle["vehicle_id"]

                    graph.add_node(
                        vehicle_id,
                        type="vehicle",
                        label=vehicle["vehicle_type"]
                    )

                    graph.add_edge(
                        profile["entity_id"],
                        vehicle_id,
                        relation="OWNS"
                    )

        # Utility

        for profile in profiles:

            aliases = profile["aliases"]

            for _, utility in self.utility_df.iterrows():

                if utility["consumer_name"] in aliases:

                    meter_id = utility["meter_id"]

                    graph.add_node(
                        meter_id,
                        type="utility",
                        label=str(
                            utility["monthly_bill"]
                        )
                    )

                    graph.add_edge(
                        profile["entity_id"],
                        meter_id,
                        relation="PAYS"
                    )

        return graph