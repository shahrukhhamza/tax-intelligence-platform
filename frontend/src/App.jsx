import { BrowserRouter, Routes, Route } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Citizens from "./pages/Citizens";
import CitizenProfile from "./pages/CitizenProfile";
import AuditReports from "./pages/AuditReports";
import KnowledgeGraphPage from "./pages/KnowledgeGraphPage";

import Sidebar from "./components/Sidebar";

import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <div className="app">

        <Sidebar />

        <main className="content">

          <header className="header">
            Tax Intelligence Platform
          </header>

          <Routes>

            <Route
              path="/"
              element={<Dashboard />}
            />

            <Route
              path="/citizens"
              element={<Citizens />}
            />

            <Route
              path="/citizen/:id"
              element={<CitizenProfile />}
            />

            {/* Full Graph View */}
            <Route
              path="/graph"
              element={<KnowledgeGraphPage />}
            />

            {/* Citizen Specific Graph */}
            <Route
              path="/graph/:id"
              element={<KnowledgeGraphPage />}
            />

            {/* Audit Reports */}
            <Route
              path="/audit"
              element={<AuditReports />}
            />

            {/* Citizen Specific Audit */}
            <Route
              path="/audit/:id"
              element={<AuditReports />}
            />

          </Routes>

        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;