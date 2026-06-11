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
    fetch(
      `http://127.0.0.1:8000/api/live-citizen/${id}`
    )
      .then((res) => res.json())
      .then((data) => {
        console.log("CITIZEN DATA:", data);
        setCitizen(data);
      });

    fetch(
      `http://127.0.0.1:8000/api/graph/${id}`
    )
      .then((res) => res.json())
      .then((data) => {
        console.log("GRAPH DATA:", data);

        setGraphData({
          nodes: data.nodes || [],
          edges: data.edges || [],
        });
      });
  }, [id]);

  if (!citizen) {
    return (
      <h2 style={{ padding: "32px" }}>
        Loading Citizen Profile...
      </h2>
    );
  }

  return (
    <div style={{ padding: "32px" }}>
      <h1>
        {citizen.name ||
          citizen.master_name ||
          "Unknown Citizen"}
      </h1>

      <h2 style={{ marginTop: "10px" }}>
        Risk Score: {citizen.risk_score || 0}
      </h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4,1fr)",
          gap: "20px",
          marginTop: "30px",
        }}
      >
        <div className="card">
          <h3>Declared Income</h3>

          <p>
            PKR{" "}
            {citizen.declared_income?.toLocaleString?.() ||
              0}
          </p>
        </div>

        <div className="card">
          <h3>Filer Status</h3>

          <p>
            {citizen.filer_status ||
              "Unknown"}
          </p>
        </div>

        <div className="card">
          <h3>Linked Records</h3>

          <p>
            {Array.isArray(
              citizen.linked_records
            )
              ? citizen.linked_records.length
              : citizen.linked_records ||
                0}
          </p>
        </div>

        <div className="card">
          <h3>Aliases</h3>

          <p>
            {citizen.aliases?.length || 0}
          </p>

          <small
            style={{
              display: "block",
              marginTop: "10px",
              color: "#666",
            }}
          >
            {citizen.aliases
              ?.slice(0, 3)
              .join(", ")}
          </small>
        </div>
      </div>

      <div
        style={{
          marginTop: "40px",
        }}
      >
        <h2>Risk Factors</h2>

        <ul
          style={{
            marginTop: "10px",
          }}
        >
          {citizen.reasons?.map(
            (reason, index) => (
              <li key={index}>
                {reason}
              </li>
            )
          )}
        </ul>
      </div>

      <div
        style={{
          display: "flex",
          gap: "15px",
          marginTop: "30px",
        }}
      >
        <button
          onClick={() =>
            navigate(`/graph/${id}`)
          }
          style={{
            padding: "12px 20px",
            cursor: "pointer",
          }}
        >
          View Full Investigation Graph
        </button>

        <button
          onClick={() =>
            navigate(`/audit/${id}`)
          }
          style={{
            padding: "12px 20px",
            cursor: "pointer",
          }}
        >
          Generate AI Audit Report
        </button>
      </div>

      <div
        style={{
          marginTop: "50px",
        }}
      >
        <h2>
          Investigation Graph
        </h2>

        <KnowledgeGraph
          nodes={graphData.nodes}
          edges={graphData.edges}
        />
      </div>
    </div>
  );
}

export default CitizenProfile;