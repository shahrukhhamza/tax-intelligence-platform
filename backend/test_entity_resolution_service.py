from services.entity_resolution_service import (
    EntityResolutionService
)

service = EntityResolutionService()

results = service.resolve_entities()

print("\nENTITY GROUPS:\n")

for entity in results[:10]:

    print(
        entity["master_name"],
        "->",
        entity["total_matches"],
        "matches"
    )

    for match in entity["matched_records"]:

        print(
            "   ",
            match["name"],
            match["confidence"]
        )

    print()