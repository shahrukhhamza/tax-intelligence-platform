import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function AuditReports() {

  const { id } = useParams();

  const [report, setReport] = useState(null);

  useEffect(() => {

    console.log(
      "AUDIT PAGE LOADED FOR:",
      id
    );

    fetch(
      `http://127.0.0.1:8000/api/audit/${id}`
    )
      .then((res) => {
        console.log(
          "STATUS:",
          res.status
        );
        return res.json();
      })
      .then((data) => {
        console.log(
          "AUDIT DATA:",
          data
        );
        setReport(data);
      })
      .catch((err) => {
        console.error(
          "AUDIT ERROR:",
          err
        );
      });

  }, [id]);

  if (!report) {
    return (
      <h1>
        Loading Audit...
      </h1>
    );
  }

  return (
    <div style={{ padding: "20px" }}>

      <h1>
        AI Audit Report
      </h1>

      <h2>
        {report.citizen}
      </h2>

      <h3>
        Tax Compliance Deviation Score: {report.risk_score}
      </h3>

      <pre>
        {JSON.stringify(
          report,
          null,
          2
        )}
      </pre>

    </div>
  );
}

export default AuditReports;