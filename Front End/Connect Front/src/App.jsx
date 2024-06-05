import { Routes, Route, Navigate } from "react-router-dom";
import { Dashboard, Auth, Login } from "@/layouts";

import { React, Suspense, useEffect, useState } from "react";

function ProtectedRoute({ children }) {
  const [Supervisor, setRole] = useState(false);

  useEffect(() => {
    setRole(sessionStorage.getItem("Supervisor"))
  }, []);

  return Supervisor ? children : <Navigate to="/dashboard/agent" replace />;
}

function App() {
  
  return (
    <Routes>
      <Route path="/dashboard/*" element={<Dashboard />} />
      <Route path="/login" element={<Login />} />
      {/* <Route path="/auth/*" element={<Auth />} /> */}
      <Route path="*" element={<ProtectedRoute children={<Navigate to="/dashboard/home" replace />} />} />
    </Routes>
  );
}

export default App;
