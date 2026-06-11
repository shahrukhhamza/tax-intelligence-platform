# Tax Intelligence Platform API Contract

## GET /api/dashboard

Response:

```json
{
  "total_citizens": 3000,
  "resolved_entities": 2870,
  "high_risk_citizens": 215,
  "potential_revenue_leakage": 125000000
}
```

---

## GET /api/citizens

Response:

```json
[
  {
    "citizen_id": "CIT001",
    "name": "Muhammad Ahmed",
    "risk_score": 94,
    "risk_level": "Critical"
  }
]
```

---

## GET /api/citizen/{id}

Response:

```json
{
  "citizen_id": "CIT001",
  "name": "Muhammad Ahmed",
  "risk_score": 94,
  "risk_level": "Critical",

  "declared_income": 450000,
  "tax_paid": 25000,
  "filer_status": "Non-Filer",

  "properties": [],

  "vehicles": [],

  "utility_bills": [],

  "travel_records": [],

  "reasons": [
    "Luxury Vehicle Ownership",
    "High Utility Consumption",
    "High Value Property"
  ]
}
```

---

## GET /api/graph/{id}

Response:

```json
{
  "nodes": [],
  "edges": []
}
```

---

## GET /api/audit/{id}

Response:

```json
{
  "risk_score": 94,

  "summary": "Potential tax compliance deviation detected.",

  "reasons": [
    "Luxury Vehicle Ownership",
    "High Utility Consumption",
    "High Value Property"
  ]
}
```

```
```
