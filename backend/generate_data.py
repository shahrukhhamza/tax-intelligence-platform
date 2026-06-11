import pandas as pd
import random

names = [
    "Muhammad Ahmed",
    "Muhammad Ahmd",
    "M Ahmed",
    "Ali Khan",
    "Aly Khan",
    "Ahmed Raza",
    "Ahmad Raza",
    "محمد احمد",
    "علی خان",
    "احمد رضا"
]

addresses = [
    "House 12 Street 10 G11 Islamabad",
    "H#12 St10 G11 Isb",
    "Street 10 G11 Islamabad",
    "House 45 DHA Lahore",
    "H#45 DHA Lhr",
    "Bahria Phase 8 Rawalpindi",
    "Phase 8 Bahria RWP"
]

vehicle_types = [
    ("Prado", 3000),
    ("Land Cruiser", 4600),
    ("Civic", 1800),
    ("Corolla", 1600),
    ("Fortuner", 2700)
]

tax_records = []
vehicle_records = []
property_records = []
utility_records = []

for i in range(1, 301):

    name = random.choice(names)
    address = random.choice(addresses)

    declared_income = random.randint(
        200000,
        3000000
    )

    tax_paid = random.randint(
        10000,
        500000
    )

    filer_status = random.choice(
        ["Filer", "Non-Filer"]
    )

    # TAX RECORD

    tax_records.append({
        "citizen_id": f"CIT{i:04}",
        "name": name,
        "address": address,
        "declared_income": declared_income,
        "tax_paid": tax_paid,
        "filer_status": filer_status
    })

    # PROPERTY

    if random.random() < 0.55:

        property_records.append({
            "property_id": f"PROP{i:04}",
            "owner_name": name,
            "address": address,
            "property_value": random.randint(
                5000000,
                30000000
            )
        })

    # VEHICLE

    if random.random() < 0.65:

        vehicle, cc = random.choice(
            vehicle_types
        )

        vehicle_records.append({
            "vehicle_id": f"VEH{i:04}",
            "owner_name": name,
            "address": address,
            "vehicle_type": vehicle,
            "engine_cc": cc
        })

    # UTILITY BILL

    if random.random() < 0.80:

        utility_records.append({
            "meter_id": f"MTR{i:04}",
            "consumer_name": name,
            "address": address,
            "monthly_bill": random.randint(
                10000,
                150000
            )
        })


# SAVE FILES

pd.DataFrame(
    tax_records
).to_csv(
    "../data/tax_records.csv",
    index=False
)

pd.DataFrame(
    vehicle_records
).to_csv(
    "../data/vehicle_records.csv",
    index=False
)

pd.DataFrame(
    property_records
).to_csv(
    "../data/property_records.csv",
    index=False
)

pd.DataFrame(
    utility_records
).to_csv(
    "../data/utility_bills.csv",
    index=False
)

print("All datasets generated successfully.")