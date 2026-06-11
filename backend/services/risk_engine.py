class RiskEngine:

    def calculate_risk(
        self,
        profile,
        vehicles=None,
        utility_bill=None
    ):

        score = 0
        reasons = []

        income = profile.get(
            "declared_income",
            0
        )

        filer_status = profile.get(
            "filer_status",
            "Unknown"
        )

        linked_records = len(
            profile.get(
                "linked_records",
                []
            )
        )

        aliases = len(
            profile.get(
                "aliases",
                []
            )
        )

        # ---------------------
        # NON FILER
        # ---------------------

        if filer_status == "Non-Filer":

            score += 25

            reasons.append(
                "Non-Filer Status"
            )

        # ---------------------
        # HIGH UTILITY BILL
        # ---------------------

        if utility_bill:

            if utility_bill > 100000:

                score += 20

                reasons.append(
                    "High Utility Consumption"
                )

            elif utility_bill > 50000:

                score += 10

                reasons.append(
                    "Moderate Utility Consumption"
                )

        # ---------------------
        # LUXURY VEHICLES
        # ---------------------

        luxury_vehicle_found = False

        if vehicles:

            for vehicle in vehicles:

                if (
                    vehicle.get(
                        "engine_cc",
                        0
                    ) >= 2500
                ):

                    luxury_vehicle_found = True
                    break

        if luxury_vehicle_found:

            score += 20

            reasons.append(
                "Luxury Vehicle Ownership"
            )

        # ---------------------
        # LOW INCOME
        # ---------------------

        if income < 500000:

            score += 15

            reasons.append(
                "Low Declared Income"
            )

        elif income < 1000000:

            score += 10

            reasons.append(
                "Moderate Declared Income"
            )

        # ---------------------
        # MULTIPLE IDENTITIES
        # ---------------------

        if aliases >= 3:

            score += 10

            reasons.append(
                "Multiple Identity Variations"
            )

        # ---------------------
        # MANY LINKED RECORDS
        # ---------------------

        if linked_records >= 5:

            score += 10

            reasons.append(
                "Multiple Linked Tax Records"
            )

        # ---------------------
        # FINAL LEVEL
        # ---------------------

        final_score = min(score, 100)

        risk_level = "Low"

        if final_score >= 75:
            risk_level = "Critical"

        elif final_score >= 50:
            risk_level = "High"

        elif final_score >= 25:
            risk_level = "Medium"

        return {

            "risk_score":
            final_score,

            "risk_level":
            risk_level,

            "reasons":
            reasons,

            "explanation":
            (
                f"Risk Score {final_score} generated due to: "
                + ", ".join(reasons)
            )

        }