import pandas as pd
import random

# -----------------------------------
# REALISTIC PAKISTANI NAMES
# -----------------------------------

names = [

    "Muhammad Ahmed",
    "Muhammad Bilal",
    "Muhammad Hamza",
    "Muhammad Usman",
    "Muhammad Talha",

    "Ali Khan",
    "Aly Khan",
    "Ali Khaan",

    "Ahmed Raza",
    "Ahmad Raza",

    "Hassan Ali",
    "Hussain Ali",
    "Adeel Malik",
    "Saqib Malik",
    "Fahad Iqbal",
    "Usman Qureshi",
    "Hamza Siddiqui",
    "Bilal Chaudhry",
    "Talha Abbasi",
    "Junaid Khan",

    "Danish Ahmed",
    "Farhan Ali",
    "Kamran Malik",
    "Waqas Khan",
    "Adnan Raza",
    "Shahzaib Ahmed",
    "Umair Khan",
    "Tariq Mehmood",
    "Salman Ahmed",
    "Asad Ali",

    "Abdullah Khan",
    "Abdul Rehman",
    "Imran Khan",
    "Faizan Ahmed",
    "Arslan Malik",
    "Khurram Shah",
    "Awais Iqbal",
    "Haris Khan",
    "Zain Ahmed",
    "Mohsin Raza",

    "Noman Ali",
    "Rizwan Khan",
    "Asim Malik",
    "Shahbaz Ahmed",
    "Jawad Hussain",
    "Sarmad Ali",
    "Irfan Khan",
    "Naveed Malik",
    "Umer Farooq",
    "Yasir Khan",

    "محمد احمد",
    "محمد بلال",
    "محمد حمزہ",
    "علی خان",
    "احمد رضا",
    "حسن علی",
    "فہد اقبال",
    "دانش احمد",
    "وقاص خان",
    "اسامہ خان"
]

# -----------------------------------
# ADDRESSES
# -----------------------------------

addresses = [

    "G-11 Islamabad",
    "G-13 Islamabad",
    "F-10 Islamabad",
    "F-11 Islamabad",
    "I-8 Islamabad",

    "Bahria Phase 7 Rawalpindi",
    "Bahria Phase 8 Rawalpindi",
    "DHA Rawalpindi",

    "Satellite Town Rawalpindi",
    "Chaklala Rawalpindi",

    "DHA Lahore",
    "Johar Town Lahore",
    "Model Town Lahore",
    "Bahria Orchard Lahore",

    "Clifton Karachi",
    "DHA Karachi",
    "Gulshan Karachi",

    "Hayatabad Peshawar",
    "University Town Peshawar",

    "Cantt Multan",
    "Wapda Town Multan",

    "Peoples Colony Faisalabad",
    "Saddar Faisalabad",

    "Jinnah Colony Sialkot",

    "Bahria Enclave Islamabad",
    "PWD Islamabad",
    "Soan Garden Islamabad"
]

vehicle_types = [

    ("Corolla", 1600),
    ("Civic", 1800),
    ("Fortuner", 2700),
    ("Prado", 3000),
    ("Land Cruiser", 4600)

]

tax_records = []
vehicle_records = []
property_records = []
utility_records = []

# -----------------------------------
# GENERATE
# -----------------------------------

for i in range(1, 301):

    name = random.choice(names)

    address = random.choice(addresses)

    declared_income = random.randint(
        500000,
        12000000
    )

    tax_paid = int(
        declared_income *
        random.uniform(0.03, 0.15)
    )

    filer_status = random.choice(
        ["Filer", "Non-Filer"]
    )

    # -----------------------------------
    # SPECIAL HIGH RISK CASES
    # -----------------------------------

    if i % 40 == 0:

        declared_income = random.randint(
            300000,
            800000
        )

        tax_paid = 0

        filer_status = "Non-Filer"

    # -----------------------------------
    # TAX RECORD
    # -----------------------------------

    tax_records.append({

        "citizen_id":
        f"CIT{i:04}",

        "name":
        name,

        "address":
        address,

        "declared_income":
        declared_income,

        "tax_paid":
        tax_paid,

        "filer_status":
        filer_status
    })

    # -----------------------------------
    # PROPERTY
    # -----------------------------------

    if random.random() < 0.45:

        property_value = random.randint(
            5000000,
            50000000
        )

        if i % 40 == 0:

            property_value = random.randint(
                30000000,
                100000000
            )

        property_records.append({

            "property_id":
            f"PROP{i:04}",

            "owner_name":
            name,

            "address":
            address,

            "property_value":
            property_value
        })

    # -----------------------------------
    # VEHICLE
    # -----------------------------------

    if random.random() < 0.60:

        vehicle, cc = random.choice(
            vehicle_types
        )

        if i % 40 == 0:

            vehicle = "Land Cruiser"
            cc = 4600

        vehicle_records.append({

            "vehicle_id":
            f"VEH{i:04}",

            "owner_name":
            name,

            "address":
            address,

            "vehicle_type":
            vehicle,

            "engine_cc":
            cc
        })

    # -----------------------------------
    # UTILITY BILL
    # -----------------------------------

    if random.random() < 0.80:

        bill = random.randint(
            10000,
            80000
        )

        if i % 40 == 0:

            bill = random.randint(
                120000,
                180000
            )

        utility_records.append({

            "meter_id":
            f"MTR{i:04}",

            "consumer_name":
            name,

            "address":
            address,

            "monthly_bill":
            bill
        })

# -----------------------------------
# SAVE FILES
# -----------------------------------

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

print("Datasets generated successfully.")