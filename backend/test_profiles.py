from services.profile_builder import (
    ProfileBuilder
)

builder = ProfileBuilder()

profiles = builder.build_profiles()

print("\nUNIFIED PROFILES\n")

for profile in profiles[:5]:

    print(
        profile["entity_id"]
    )

    print(
        profile["master_name"]
    )

    print(
        profile["aliases"]
    )

    print(
        profile["linked_records"]
    )

    print("-" * 40)