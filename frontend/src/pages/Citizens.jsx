import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

function Citizens() {
  const [citizens, setCitizens] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/live-citizens")
      .then((res) => res.json())
      .then((data) => setCitizens(data))
      .catch((err) => console.error(err));
  }, []);

  const filteredCitizens = useMemo(() => {
    return citizens.filter((citizen) => {
      const term = search.toLowerCase();

      return (
        citizen.name?.toLowerCase().includes(term) ||
        citizen.entity_id?.toLowerCase().includes(term)
      );
    });
  }, [citizens, search]);

  const getRiskBadge = (level) => {
    const styles = {
      Critical: {
        background: "rgba(239,68,68,0.15)",
        color: "#EF4444",
      },
      High: {
        background: "rgba(249,115,22,0.15)",
        color: "#F97316",
      },
      Medium: {
        background: "rgba(234,179,8,0.15)",
        color: "#EAB308",
      },
      Low: {
        background: "rgba(34,197,94,0.15)",
        color: "#22C55E",
      },
    };

    const style = styles[level] || styles.Low;

    return (
      <span
        style={{
          padding: "6px 12px",
          borderRadius: "999px",
          fontSize: "12px",
          fontWeight: "700",
          ...style,
        }}
      >
        {level}
      </span>
    );
  };

  return (
    <div style={{ padding: "32px" }}>
      {/* Header */}

      <div
        style={{
          marginBottom: "30px",
        }}
      >
        <h1>Entity Explorer</h1>

        <p
          style={{
            color: "#94A3B8",
            marginTop: "10px",
          }}
        >
          Search and investigate resolved entities across
          integrated tax datasets.
        </p>
      </div>

      {/* Search */}

      <div
        className="card"
        style={{
          padding: "20px",
          marginBottom: "25px",
        }}
      >
        <input
          type="text"
          placeholder="Search by Name or Entity ID..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{
            width: "100%",
            padding: "14px",
            borderRadius: "12px",
            border: "1px solid #243244",
            background: "#0F172A",
            color: "#fff",
            outline: "none",
          }}
        />
      </div>

      {/* Stats */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(220px,1fr))",
          gap: "20px",
          marginBottom: "25px",
        }}
      >
        <div className="card" style={{ padding: "20px" }}>
          <h3>Total Entities</h3>
          <h1>{citizens.length}</h1>
        </div>

        <div className="card" style={{ padding: "20px" }}>
          <h3>Search Results</h3>
          <h1>{filteredCitizens.length}</h1>
        </div>
      </div>

      {/* Table */}

      <div
        className="card"
        style={{
          overflow: "hidden",
        }}
      >
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
          }}
        >
          <thead>
            <tr
              style={{
                background: "rgba(255,255,255,0.03)",
              }}
            >
              <th style={thStyle}>Entity ID</th>
              <th style={thStyle}>Name</th>
              <th style={thStyle}>Risk Score</th>
              <th style={thStyle}>Risk Level</th>
            </tr>
          </thead>

          <tbody>
            {filteredCitizens.map((citizen) => (
              <tr
                key={citizen.entity_id}
                style={{
                  borderTop:
                    "1px solid rgba(255,255,255,0.05)",
                }}
              >
                <td style={tdStyle}>
                  {citizen.entity_id}
                </td>

                <td style={tdStyle}>
                  <Link
                    to={`/citizen/${citizen.entity_id}`}
                    style={{
                      color: "#60A5FA",
                      fontWeight: "600",
                    }}
                  >
                    {citizen.name}
                  </Link>
                </td>

                <td style={tdStyle}>
                  {citizen.risk_score}
                </td>

                <td style={tdStyle}>
                  {getRiskBadge(
                    citizen.risk_level
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const thStyle = {
  textAlign: "left",
  padding: "16px",
  color: "#94A3B8",
  fontSize: "13px",
  letterSpacing: "1px",
  textTransform: "uppercase",
};

const tdStyle = {
  padding: "16px",
};

export default Citizens;