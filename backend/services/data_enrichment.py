import pandas as pd

from services.entity_resolution import EntityResolver


class DataEnrichment:

    def __init__(self):

        self.resolver = EntityResolver()

        self.vehicle_df = pd.read_csv(
            "../data/vehicle_records.csv"
        )

        self.utility_df = pd.read_csv(
            "../data/utility_bills.csv"
        )

    def enrich(self, profile):

        aliases = profile["aliases"]

        matched_vehicles = []

        matched_bills = []

        max_bill = 0

        # -----------------------------
        # VEHICLES
        # -----------------------------

        for _, vehicle in self.vehicle_df.iterrows():

            owner_name = vehicle["owner_name"]

            matched = False

            for alias in aliases:

                score = (
                    self.resolver
                    .calculate_similarity(
                        alias,
                        owner_name
                    )
                )

                if score >= 80:

                    matched = True
                    break

            if matched:

                matched_vehicles.append({
                    "vehicle_id":
                    vehicle["vehicle_id"],

                    "vehicle_type":
                    vehicle["vehicle_type"],

                    "engine_cc":
                    int(vehicle["engine_cc"])
                })

        # -----------------------------
        # UTILITY BILLS
        # -----------------------------

        for _, utility in self.utility_df.iterrows():

            consumer_name = utility[
                "consumer_name"
            ]

            matched = False

            for alias in aliases:

                score = (
                    self.resolver
                    .calculate_similarity(
                        alias,
                        consumer_name
                    )
                )

                if score >= 80:

                    matched = True
                    break

            if matched:

                bill = int(
                    utility["monthly_bill"]
                )

                matched_bills.append(bill)

                if bill > max_bill:
                    max_bill = bill

        return {

            "vehicles":
            matched_vehicles,

            "utility_bills":
            matched_bills,

            "max_bill":
            max_bill,

            "vehicle_count":
            len(matched_vehicles),

            "luxury_vehicle_count":
            len([
                v
                for v in matched_vehicles
                if v["engine_cc"] >= 2500
            ])
        }