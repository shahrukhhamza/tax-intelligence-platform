from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.citizens import router as citizens_router
from routes.graph import router as graph_router
from routes.audit import router as audit_router


app = FastAPI(
    title="Tax Intelligence Platform",
    description="Graph AI for Broadening the National Tax Net",
    version="1.0.0"
)

# ----------------------------------
# CORS
# ----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------
# ROUTERS
# ----------------------------------

app.include_router(
    citizens_router,
    prefix="/api"
)

app.include_router(
    graph_router,
    prefix="/api"
)

app.include_router(
    audit_router,
    prefix="/api"
)

# ----------------------------------
# ROOT
# ----------------------------------

@app.get("/")
def root():

    return {
        "message":
        "Tax Intelligence Platform API Running"
    }


# ----------------------------------
# TEMP DASHBOARD TEST
# ----------------------------------

@app.get("/api/dashboard")
def dashboard():

    return {

        "total_citizens":
        301,

        "resolved_entities":
        301,

        "high_risk_citizens":
        47,

        "average_risk_score":
        56.4,

        "potential_revenue_leakage":
        12500000

    }


# ----------------------------------
# LEGACY DEMO ENDPOINTS
# ----------------------------------

@app.get("/api/citizens-demo")
def get_demo_citizens():

    return [

        {
            "citizen_id":
            "CIT001",

            "name":
            "Muhammad Ahmed",

            "risk_score":
            94,

            "risk_level":
            "Critical"
        },

        {
            "citizen_id":
            "CIT002",

            "name":
            "Ali Khan",

            "risk_score":
            82,

            "risk_level":
            "High"
        },

        {
            "citizen_id":
            "CIT003",

            "name":
            "Ahmed Raza",

            "risk_score":
            45,

            "risk_level":
            "Medium"
        }
    ]


@app.get("/api/citizen-demo/{citizen_id}")
def get_demo_citizen(
    citizen_id: str
):

    return {

        "citizen_id":
        citizen_id,

        "name":
        "Muhammad Ahmed",

        "risk_score":
        94,

        "risk_level":
        "Critical",

        "declared_income":
        450000,

        "tax_paid":
        25000,

        "filer_status":
        "Non-Filer"
    }


@app.get("/api/graph-demo/{citizen_id}")
def get_demo_graph(
    citizen_id: str
):

    return {

        "nodes": [

            {
                "id":
                "citizen_1",

                "label":
                "Muhammad Ahmed",

                "type":
                "citizen"
            },

            {
                "id":
                "vehicle_1",

                "label":
                "Toyota Prado",

                "type":
                "vehicle"
            }
        ],

        "edges": [

            {
                "source":
                "citizen_1",

                "target":
                "vehicle_1",

                "label":
                "OWNS"
            }
        ]
    }


@app.get("/api/audit-demo/{citizen_id}")
def get_demo_audit(
    citizen_id: str
):

    return {

        "risk_score":
        94,

        "summary":
        "Potential tax compliance deviation detected.",

        "reasons": [

            "Luxury Vehicle Ownership",

            "High Utility Consumption",

            "High Value Property"
        ]
    }