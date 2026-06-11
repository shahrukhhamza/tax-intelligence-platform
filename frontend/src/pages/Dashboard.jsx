import { useEffect, useState } from "react";

function Dashboard() {

  const [stats, setStats] = useState(null);

  useEffect(() => {

    fetch(
      "http://127.0.0.1:8000/api/dashboard"
    )
      .then((res) => res.json())
      .then((data) => {
        setStats(data);
      });

  }, []);

  if (!stats) {
    return (
      <h2 style={{ padding: "20px" }}>
        Loading Dashboard...
      </h2>
    );
  }

  return (
    <>
      <section className="metrics">

        <div className="card">
          <h3>Total Tax Records</h3>
          <p>{stats.total_citizens}</p>
        </div>

        <div className="card">
          <h3>Resolved Entities</h3>
          <p>{stats.resolved_entities}</p>
        </div>

        <div className="card">
          <h3>High Risk Citizens</h3>
          <p>{stats.high_risk_citizens}</p>
        </div>

        <div className="card">
          <h3>Potential Revenue Leakage</h3>
          <p>
            PKR{" "}
            {stats.potential_revenue_leakage?.toLocaleString()}
          </p>
        </div>

      </section>
    </>
  );
}

export default Dashboard;