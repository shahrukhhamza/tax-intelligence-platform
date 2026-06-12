class RiskEngine:

    def calculate_risk(
        self,
        profile,
        vehicles=None,
        utility_bill=None,
        properties=None
    ):

        score = 0

        reasons = []

        income = profile.get(
            "declared_income",
            0
        )

        tax_paid = profile.get(
            "tax_paid",
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

        # --------------------------------
        # FILER STATUS
        # --------------------------------

        if filer_status == "Non-Filer":

            score += 25

            reasons.append(
                "Registered as Non-Filer"
            )

        # --------------------------------
        # TAX RATIO
        # --------------------------------

        if income > 0:

            tax_ratio = (
                tax_paid / income
            ) * 100

            if tax_ratio < 1:

                score += 30

                reasons.append(
                    f"Extremely low tax ratio ({tax_ratio:.2f}%)"
                )

            elif tax_ratio < 3:

                score += 20

                reasons.append(
                    f"Low tax ratio ({tax_ratio:.2f}%)"
                )

            elif tax_ratio < 8:

                score += 10

                reasons.append(
                    f"Moderate tax ratio ({tax_ratio:.2f}%)"
                )

        # --------------------------------
        # UTILITY BILL
        # --------------------------------

        if utility_bill:

            if utility_bill > 150000:

                score += 20

                reasons.append(
                    f"Very high utility bill (PKR {utility_bill:,})"
                )

            elif utility_bill > 100000:

                score += 15

                reasons.append(
                    f"High utility bill (PKR {utility_bill:,})"
                )

            elif utility_bill > 60000:

                score += 8

                reasons.append(
                    f"Moderate utility bill (PKR {utility_bill:,})"
                )

        # --------------------------------
        # VEHICLES
        # --------------------------------

        luxury_count = 0

        if vehicles:

            for vehicle in vehicles:

                if (
                    vehicle.get(
                        "engine_cc",
                        0
                    ) >= 2500
                ):

                    luxury_count += 1

        if luxury_count >= 4:

            score += 25

            reasons.append(
                f"Owns {luxury_count} luxury vehicles"
            )

        elif luxury_count >= 2:

            score += 15

            reasons.append(
                f"Owns {luxury_count} luxury vehicles"
            )

        elif luxury_count == 1:

            score += 8

            reasons.append(
                "Owns luxury vehicle"
            )

        # --------------------------------
        # PROPERTIES
        # --------------------------------

        property_count = 0

        if properties:

            property_count = len(
                properties
            )

        if property_count >= 4:

            score += 20

            reasons.append(
                f"Owns {property_count} properties"
            )

        elif property_count >= 2:

            score += 10

            reasons.append(
                f"Owns {property_count} properties"
            )

        elif property_count == 1:

            score += 5

            reasons.append(
                "Owns property assets"
            )

        # --------------------------------
        # ALIASES
        # --------------------------------

        if aliases >= 5:

            score += 12

            reasons.append(
                "Many identity variations detected"
            )

        elif aliases >= 3:

            score += 6

            reasons.append(
                "Multiple identity variations detected"
            )

        # --------------------------------
        # LINKED RECORDS
        # --------------------------------

        if linked_records >= 8:

            score += 10

            reasons.append(
                "Large number of linked records"
            )

        elif linked_records >= 4:

            score += 5

            reasons.append(
                "Multiple linked records"
            )

        # --------------------------------
        # LIFESTYLE MISMATCH
        # --------------------------------

        if (
            income < 1000000
            and utility_bill
            and utility_bill > 100000
        ):

            score += 20

            reasons.append(
                "Lifestyle inconsistent with declared income"
            )

        # --------------------------------
        # HIGH INCOME
        # --------------------------------

        if income > 8000000:

            score += 5

            reasons.append(
                "High-income taxpayer"
            )

        # --------------------------------
        # FINAL
        # --------------------------------

        final_score = min(
            score,
            100
        )

        if final_score >= 80:

            risk_level = "Critical"

        elif final_score >= 60:

            risk_level = "High"

        elif final_score >= 35:

            risk_level = "Medium"

        else:

            risk_level = "Low"

        return {

            "risk_score":
            final_score,

            "tax_compliance_deviation_score":
            final_score,

            "risk_level":
            risk_level,

            "reasons":
            reasons,

            "explanation":
            (
                f"Tax Compliance Deviation Score "
                f"{final_score}/100 generated due to: "
                + ", ".join(reasons)
            )

        }