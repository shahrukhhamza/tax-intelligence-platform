from rapidfuzz import fuzz
from services.normalization import normalize_text


class EntityResolver:

    def normalize_name(self, name):
        """
        Normalize names before comparison
        """
        return normalize_text(name)

    def calculate_similarity(self, name1, name2):
        """
        Fuzzy similarity score between two names
        """

        n1 = self.normalize_name(name1)
        n2 = self.normalize_name(name2)

        return fuzz.token_sort_ratio(n1, n2)

    def calculate_combined_score(
        self,
        name1,
        name2,
        address1="",
        address2=""
    ):
        """
        Future-ready combined score
        """

        name_score = fuzz.token_sort_ratio(
            self.normalize_name(name1),
            self.normalize_name(name2)
        )

        if address1 and address2:

            address_score = fuzz.token_sort_ratio(
                normalize_text(address1),
                normalize_text(address2)
            )

            final_score = (
                name_score * 0.7 +
                address_score * 0.3
            )

            return round(final_score, 2)

        return round(name_score, 2)

    def find_matches(
        self,
        target_name,
        candidate_names,
        threshold=75
    ):
        """
        Return matching candidates
        """

        matches = []

        for candidate in candidate_names:

            score = self.calculate_similarity(
                target_name,
                candidate
            )

            if score >= threshold:

                matches.append({
                    "name": candidate,
                    "confidence": round(score, 2)
                })

        matches.sort(
            key=lambda x: x["confidence"],
            reverse=True
        )

        return matches