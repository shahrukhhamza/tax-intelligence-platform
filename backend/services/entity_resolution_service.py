import pandas as pd
from services.entity_resolution import EntityResolver


class EntityResolutionService:

    def __init__(self):

        self.resolver = EntityResolver()

        self.tax_df = pd.read_csv(
            "../data/tax_records.csv"
        )

    def resolve_entities(self):

        entities = []

        processed = set()

        records = self.tax_df.to_dict(
            orient="records"
        )

        for record in records:

            citizen_id = record["citizen_id"]

            if citizen_id in processed:
                continue

            matches = []

            for candidate in records:

                candidate_id = candidate["citizen_id"]

                if candidate_id == citizen_id:
                    continue

                score = self.resolver.calculate_similarity(
                    record["name"],
                    candidate["name"]
                )

                if score >= 85:

                    matches.append({
                        "citizen_id": candidate_id,
                        "name": candidate["name"],
                        "confidence": round(score, 2)
                    })

                    processed.add(candidate_id)

            entities.append({

                "master_id": citizen_id,

                "master_name": record["name"],

                "matched_records": matches,

                "total_matches": len(matches)
            })

            processed.add(citizen_id)

        return entities