import { useEffect, useState } from "react";

function AuditReports() {

  const [report, setReport] = useState(null);

  useEffect(() => {

    console.log("AUDIT PAGE LOADED");

    fetch("http://127.0.0.1:8000/api/audit/ENT001")
      .then((res) => {
        console.log("STATUS:", res.status);
        return res.json();
      })
      .then((data) => {
        console.log("AUDIT DATA:", data);
        setReport(data);
      })
      .catch((err) => {
        console.error("AUDIT ERROR:", err);
      });

  }, []);

  if (!report) {
    return <h1>Loading Audit...</h1>;
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>Audit Working</h1>

      <pre>
        {JSON.stringify(report, null, 2)}
      </pre>
    </div>
  );
}

export default AuditReports;