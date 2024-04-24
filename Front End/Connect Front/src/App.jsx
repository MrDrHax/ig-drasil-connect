import { Routes, Route, Navigate } from "react-router-dom";
import { Dashboard, Auth, Login } from "@/layouts";
import { validateToken, getApiLoginPage } from "@/configs";

function App() {
  

  return (
    <Routes>
      <Route path="/dashboard/*" element={<Dashboard />} />
      <Route path="/login" element={<Login />} />
      {/* <Route path="/auth/*" element={<Auth />} /> */}
      <Route path="*" element={<Navigate to="/dashboard/home" replace />} />
    </Routes>
  );
}

export default App;
