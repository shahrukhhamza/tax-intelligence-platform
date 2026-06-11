import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function Citizens() {
  const [citizens, setCitizens] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/live-citizens")
      .then((res) => res.json())
      .then((data) => setCitizens(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div style={{ padding: "32px" }}>
      <h2 style={{ marginBottom: "20px" }}>
        Citizens
      </h2>

      <table>
        <thead>
          <tr>
            <th>Entity ID</th>
            <th>Name</th>
            <th>Risk Score</th>
            <th>Risk Level</th>
          </tr>
        </thead>

        <tbody>
          {citizens.map((citizen) => (
            <tr key={citizen.entity_id}>
              <td>{citizen.entity_id}</td>

              <td>
                <Link
                  to={`/citizen/${citizen.entity_id}`}
                >
                  {citizen.name}
                </Link>
              </td>

              <td>{citizen.risk_score}</td>

              <td>{citizen.risk_level}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Citizens;