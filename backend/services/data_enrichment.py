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

        self.property_df = pd.read_csv(
            "../data/property_records.csv"
        )

        # ----------------------------------
        # CACHE
        # ----------------------------------

        self._cache = {}

    def enrich(self, profile):

        # ----------------------------------
        # CACHE HIT
        # ----------------------------------

        cache_key = profile["entity_id"]

        if cache_key in self._cache:

            return self._cache[cache_key]

        aliases = profile["aliases"]

        matched_vehicles = []
        matched_bills = []
        matched_properties = []

        max_bill = 0

        seen_vehicles = set()
        seen_bills = set()
        seen_properties = set()

        # ----------------------------------
        # VEHICLE MATCHING
        # ----------------------------------

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

                if score >= 92:

                    matched = True
                    break

            if matched:

                vehicle_id = vehicle["vehicle_id"]

                if vehicle_id not in seen_vehicles:

                    seen_vehicles.add(
                        vehicle_id
                    )

                    matched_vehicles.append({

                        "vehicle_id":
                        vehicle_id,

                        "vehicle_type":
                        vehicle["vehicle_type"],

                        "engine_cc":
                        int(
                            vehicle["engine_cc"]
                        )
                    })

        # ----------------------------------
        # UTILITY MATCHING
        # ----------------------------------

        for _, utility in self.utility_df.iterrows():

            consumer_name = (
                utility["consumer_name"]
            )

            matched = False

            for alias in aliases:

                score = (
                    self.resolver
                    .calculate_similarity(
                        alias,
                        consumer_name
                    )
                )

                if score >= 92:

                    matched = True
                    break

            if matched:

                bill = int(
                    utility["monthly_bill"]
                )

                if bill not in seen_bills:

                    seen_bills.add(
                        bill
                    )

                    matched_bills.append(
                        bill
                    )

                if bill > max_bill:

                    max_bill = bill

        # ----------------------------------
        # PROPERTY MATCHING
        # ----------------------------------

        for _, property_record in self.property_df.iterrows():

            owner_name = (
                property_record["owner_name"]
            )

            matched = False

            for alias in aliases:

                score = (
                    self.resolver
                    .calculate_similarity(
                        alias,
                        owner_name
                    )
                )

                if score >= 92:

                    matched = True
                    break

            if matched:

                property_id = (
                    property_record[
                        "property_id"
                    ]
                )

                if property_id not in seen_properties:

                    seen_properties.add(
                        property_id
                    )

                    matched_properties.append({

                        "property_id":
                        property_id,

                        "property_type":
                        property_record.get(
                            "property_type",
                            "Unknown"
                        )
                    })

        # ----------------------------------
        # LUXURY VEHICLES
        # ----------------------------------

        luxury_vehicle_count = len([

            vehicle

            for vehicle in matched_vehicles

            if vehicle["engine_cc"] >= 2000

        ])

        result = {

            "vehicles":
            matched_vehicles,

            "properties":
            matched_properties,

            "utility_bills":
            matched_bills,

            "max_bill":
            max_bill,

            "vehicle_count":
            len(
                matched_vehicles
            ),

            "property_count":
            len(
                matched_properties
            ),

            "luxury_vehicle_count":
            luxury_vehicle_count
        }

        # ----------------------------------
        # SAVE TO CACHE
        # ----------------------------------

        self._cache[cache_key] = result

        return result