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

        # ---------------------
        # NON FILER
        # ---------------------

        if filer_status == "Non-Filer":

            score += 25

            reasons.append(
                "Registered as Non-Filer"
            )

        # ---------------------
        # TAX TO INCOME RATIO
        # ---------------------

        if income > 0:

            tax_ratio = (
                tax_paid / income
            ) * 100

            if tax_ratio < 2:

                score += 25

                reasons.append(
                    f"Very low tax-to-income ratio ({tax_ratio:.2f}%)"
                )

            elif tax_ratio < 5:

                score += 15

                reasons.append(
                    f"Low tax-to-income ratio ({tax_ratio:.2f}%)"
                )

        # ---------------------
        # HIGH UTILITY BILL
        # ---------------------

        if utility_bill:

            if utility_bill > 100000:

                score += 20

                reasons.append(
                    f"High utility consumption (PKR {utility_bill:,})"
                )

            elif utility_bill > 50000:

                score += 10

                reasons.append(
                    f"Moderate utility consumption (PKR {utility_bill:,})"
                )

        # ---------------------
        # LUXURY VEHICLES
        # ---------------------

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

        if luxury_count >= 1:

            score += 20

            reasons.append(
                f"Owns {luxury_count} luxury vehicle(s)"
            )

        # ---------------------
        # MULTIPLE IDENTITIES
        # ---------------------

        if aliases >= 3:

            score += 10

            reasons.append(
                "Multiple identity variations detected"
            )

        # ---------------------
        # MANY LINKED RECORDS
        # ---------------------

        if linked_records >= 5:

            score += 10

            reasons.append(
                "Large number of linked records"
            )

        # ---------------------
        # INCOME VS LIFESTYLE
        # ---------------------

        if (
            income < 1000000
            and utility_bill
            and utility_bill > 100000
        ):

            score += 15

            reasons.append(
                "Lifestyle appears inconsistent with declared income"
            )

        # ---------------------
        # FINAL SCORE
        # ---------------------

        final_score = min(
            score,
            100
        )

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