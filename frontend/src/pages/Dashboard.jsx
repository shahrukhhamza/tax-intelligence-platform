import { useEffect, useState } from "react";

function Dashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/dashboard")
      .then((res) => res.json())
      .then((data) => setStats(data))
      .catch((err) => console.error(err));
  }, []);

  if (!stats) {
    return (
      <div style={{ padding: "40px" }}>
        <h2>Loading Dashboard...</h2>
      </div>
    );
  }

  const cardStyle = {
    background: "#111827",
    border: "1px solid #243244",
    borderRadius: "20px",
    padding: "24px",
  };

  return (
    <div style={{ padding: "32px" }}>
      {/* HERO */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "2fr 1fr",
          gap: "24px",
          marginBottom: "30px",
        }}
      >
        <div style={cardStyle}>
          <div
            style={{
              color: "#3B82F6",
              fontSize: "12px",
              letterSpacing: "2px",
              textTransform: "uppercase",
              marginBottom: "12px",
            }}
          >
            National Tax Intelligence Platform
          </div>

          <h1
            style={{
              marginBottom: "16px",
            }}
          >
            Tax Intelligence Command Center
          </h1>

          <p
            style={{
              color: "#94A3B8",
              lineHeight: "1.8",
              maxWidth: "800px",
            }}
          >
            AI-powered entity resolution, graph analytics,
            compliance intelligence and audit automation
            platform designed to identify hidden tax risk,
            recover revenue leakage and broaden the national
            tax net.
          </p>
        </div>

        <div
          style={{
            ...cardStyle,
            background:
              "linear-gradient(135deg,#450A0A,#7F1D1D)",
          }}
        >
          <div
            style={{
              color: "#FCA5A5",
              fontSize: "13px",
              marginBottom: "10px",
            }}
          >
            Potential Recovery
          </div>

          <div
            style={{
              fontSize: "42px",
              fontWeight: "800",
              color: "#ffffff",
            }}
          >
            PKR {(stats.potential_revenue_leakage / 1000000).toFixed(1)}M
          </div>

          <div
            style={{
              marginTop: "12px",
              color: "#FECACA",
            }}
          >
            Revenue Leakage Detected
          </div>
        </div>
      </div>

      {/* KPI ROW */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(250px,1fr))",
          gap: "20px",
          marginBottom: "30px",
        }}
      >
        <div style={cardStyle}>
          <div
            style={{
              fontSize: "48px",
              fontWeight: "800",
            }}
          >
            {stats.total_citizens}
          </div>

          <div style={{ color: "#94A3B8" }}>
            Total Citizens
          </div>
        </div>

        <div style={cardStyle}>
          <div
            style={{
              fontSize: "48px",
              fontWeight: "800",
            }}
          >
            {stats.resolved_entities}
          </div>

          <div style={{ color: "#94A3B8" }}>
            Resolved Entities
          </div>
        </div>

        <div style={cardStyle}>
          <div
            style={{
              fontSize: "48px",
              fontWeight: "800",
              color: "#EF4444",
            }}
          >
            {stats.high_risk_citizens}
          </div>

          <div style={{ color: "#94A3B8" }}>
            High Risk Citizens
          </div>
        </div>

        <div style={cardStyle}>
          <div
            style={{
              fontSize: "48px",
              fontWeight: "800",
            }}
          >
            {stats.average_risk_score}
          </div>

          <div style={{ color: "#94A3B8" }}>
            Average Risk Score
          </div>
        </div>
      </div>

      {/* PIPELINE + ALERTS */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "2fr 1fr",
          gap: "24px",
          marginBottom: "30px",
        }}
      >
        <div style={cardStyle}>
          <h2 style={{ marginBottom: "24px" }}>
            Intelligence Pipeline
          </h2>

          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              flexWrap: "wrap",
              gap: "16px",
            }}
          >
            {[
              "Tax Records",
              "Entity Resolution",
              "Knowledge Graph",
              "Risk Engine",
              "AI Audit",
            ].map((step) => (
              <div
                key={step}
                style={{
                  flex: 1,
                  minWidth: "140px",
                  textAlign: "center",
                  padding: "16px",
                  borderRadius: "12px",
                  background: "#0F172A",
                  border: "1px solid #243244",
                }}
              >
                {step}
              </div>
            ))}
          </div>
        </div>

        <div style={cardStyle}>
          <h2
            style={{
              marginBottom: "20px",
            }}
          >
            Critical Alerts
          </h2>

          <div style={{ color: "#EF4444" }}>
            ● Faizan Ahmed — Risk 100
          </div>

          <div
            style={{
              color: "#F97316",
              marginTop: "10px",
            }}
          >
            ● Ali Khan — Risk 99
          </div>

          <div
            style={{
              color: "#EAB308",
              marginTop: "10px",
            }}
          >
            ● Tariq Mehmood — Risk 95
          </div>

          <div
            style={{
              marginTop: "20px",
              color: "#94A3B8",
            }}
          >
            Priority Audit Recommended
          </div>
        </div>
      </div>

      {/* DATA SOURCES */}

      <div style={cardStyle}>
        <h2
          style={{
            marginBottom: "24px",
          }}
        >
          Connected Data Sources
        </h2>

        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit,minmax(220px,1fr))",
            gap: "20px",
          }}
        >
          <div style={cardStyle}>
            <h1>301</h1>
            <p style={{ color: "#94A3B8" }}>
              Tax Records
            </p>
          </div>

          <div style={cardStyle}>
            <h1>195</h1>
            <p style={{ color: "#94A3B8" }}>
              Vehicle Records
            </p>
          </div>

          <div style={cardStyle}>
            <h1>245</h1>
            <p style={{ color: "#94A3B8" }}>
              Utility Bills
            </p>
          </div>

          <div style={cardStyle}>
            <h1>140</h1>
            <p style={{ color: "#94A3B8" }}>
              Property Records
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;