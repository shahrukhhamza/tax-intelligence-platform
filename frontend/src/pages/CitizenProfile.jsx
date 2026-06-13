import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import KnowledgeGraph from "../components/KnowledgeGraph";

function CitizenProfile() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [citizen, setCitizen] = useState(null);
  const [graphData, setGraphData] = useState({
    nodes: [],
    edges: [],
  });

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/live-citizen/${id}`)
      .then((res) => res.json())
      .then((data) => setCitizen(data))
      .catch(console.error);

    fetch(`http://127.0.0.1:8000/api/graph/${id}`)
      .then((res) => res.json())
      .then((data) =>
        setGraphData({
          nodes: data.nodes || [],
          edges: data.edges || [],
        })
      )
      .catch(console.error);
  }, [id]);

  if (!citizen) {
    return (
      <div style={{ padding: "32px" }}>
        <h2>Loading Citizen Profile...</h2>
      </div>
    );
  }

  const riskColor =
    citizen.risk_score >= 80
      ? "#EF4444"
      : citizen.risk_score >= 60
      ? "#F97316"
      : citizen.risk_score >= 35
      ? "#EAB308"
      : "#22C55E";

  return (
    <div style={{ padding: "32px" }}>
      <h1>{citizen.name}</h1>

      <p style={{ color: "#94A3B8", marginTop: "8px" }}>
        Entity ID: {citizen.entity_id}
      </p>

      {/* Risk Score */}
      <div
        className="card"
        style={{
          padding: "24px",
          marginTop: "24px",
          marginBottom: "24px",
        }}
      >
        <h3>Tax Compliance Deviation Score</h3>

        <h1
          style={{
            color: riskColor,
            marginTop: "10px",
          }}
        >
          {citizen.risk_score}/100
        </h1>

        <p style={{ color: riskColor }}>
          {citizen.risk_level} Risk
        </p>
      </div>

      {/* Metrics */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(220px,1fr))",
          gap: "20px",
          marginBottom: "30px",
        }}
      >
        <div className="card" style={{ padding: "20px" }}>
          <h3>Declared Income</h3>
          <p>
            PKR{" "}
            {citizen.declared_income?.toLocaleString()}
          </p>
        </div>

        <div className="card" style={{ padding: "20px" }}>
          <h3>Filer Status</h3>
          <p>{citizen.filer_status}</p>
        </div>

        <div className="card" style={{ padding: "20px" }}>
          <h3>Vehicles</h3>
          <p>{citizen.vehicle_count}</p>
        </div>

        <div className="card" style={{ padding: "20px" }}>
          <h3>Properties</h3>
          <p>{citizen.property_count}</p>
        </div>
      </div>

      {/* Risk Factors */}
      <div
        className="card"
        style={{
          padding: "24px",
          marginBottom: "30px",
        }}
      >
        <h2>Risk Factors</h2>

        <ul style={{ marginTop: "16px" }}>
          {citizen.reasons?.map((reason, index) => (
            <li key={index}>{reason}</li>
          ))}
        </ul>
      </div>

      {/* Entity Resolution */}
      <div
        className="card"
        style={{
          padding: "24px",
          marginBottom: "30px",
        }}
      >
        <h2>Entity Resolution</h2>

        <p style={{ marginTop: "12px" }}>
          Linked Records:{" "}
          {citizen.linked_records?.length || 0}
        </p>

        <p>
          Identity Variations:{" "}
          {citizen.aliases?.length || 0}
        </p>

        <p>
          Aliases:{" "}
          {citizen.aliases?.join(", ")}
        </p>
      </div>

      {/* Actions */}
      <div
        style={{
          display: "flex",
          gap: "15px",
          marginBottom: "40px",
          flexWrap: "wrap",
        }}
      >
        <button
          className="btn button-primary"
          onClick={() =>
            navigate(`/graph/${id}`)
          }
        >
          Investigation Graph
        </button>

        <button
          className="btn button-danger"
          onClick={() =>
            navigate(`/audit/${id}`)
          }
        >
          Generate AI Audit Report
        </button>
      </div>

      {/* Graph */}
      <div
        className="card"
        style={{
          padding: "24px",
        }}
      >
        <h2>Investigation Network</h2>

        <div style={{ marginTop: "20px" }}>
          <KnowledgeGraph
            nodes={graphData.nodes}
            edges={graphData.edges}
          />
        </div>
      </div>
    </div>
  );
}

export default CitizenProfile;