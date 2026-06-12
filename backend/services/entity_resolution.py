from rapidfuzz import fuzz
from services.normalization import normalize_text


class EntityResolver:

    def normalize_name(
        self,
        name
    ):

        return normalize_text(
            str(name)
        )

    # -----------------------------
    # NAME SIMILARITY
    # -----------------------------

    def calculate_similarity(
        self,
        name1,
        name2
    ):

        n1 = self.normalize_name(
            name1
        )

        n2 = self.normalize_name(
            name2
        )

        return fuzz.token_sort_ratio(
            n1,
            n2
        )

    # -----------------------------
    # COMBINED SCORE
    # -----------------------------

    def calculate_combined_score(

        self,

        name1,
        name2,

        address1="",
        address2=""

    ):

        name_score = (
            fuzz.token_sort_ratio(

                self.normalize_name(
                    name1
                ),

                self.normalize_name(
                    name2
                )
            )
        )

        # -------------------------
        # ADDRESS SCORE
        # -------------------------

        address_score = 0

        if address1 and address2:

            address_score = (
                fuzz.token_sort_ratio(

                    normalize_text(
                        str(address1)
                    ),

                    normalize_text(
                        str(address2)
                    )
                )
            )

        # -------------------------
        # WEIGHTED SCORE
        # -------------------------

        final_score = (

            name_score * 0.75 +

            address_score * 0.25

        )

        return round(
            final_score,
            2
        )

    # -----------------------------
    # MATCH SEARCH
    # -----------------------------

    def find_matches(

        self,

        target_name,

        candidate_names,

        threshold=90

    ):

        matches = []

        for candidate in candidate_names:

            score = (
                self.calculate_similarity(
                    target_name,
                    candidate
                )
            )

            if score >= threshold:

                matches.append({

                    "name":
                    candidate,

                    "confidence":
                    round(score, 2)

                })

        matches.sort(

            key=lambda x:
            x["confidence"],

            reverse=True

        )

        return matches