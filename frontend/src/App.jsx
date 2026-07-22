import { BrowserRouter, Routes, Route } from "react-router-dom";
import Settings from "./pages/Settings";
import Login from "./pages/Login";
import Terms from "./pages/Terms";
import PrivacyPolicy from "./pages/PrivacyPolicy";
import Dashboard from "./pages/Dashboard";
import Profile from "./pages/Profile";
import OAuthCallback from "./pages/OAuthCallback";
import ProtectedRoute from "./components/common/ProtectedRoute";
import ManageReminders from "./pages/ManageReminders";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          }
        />

        <Route
          path="/settings"
          element={
            <ProtectedRoute>
              <Settings />
            </ProtectedRoute>
          }
        />

        <Route
          path="/manage-reminders"
          element={
            <ProtectedRoute>
              <ManageReminders />
            </ProtectedRoute>
          }
        />
        <Route path="/terms" element={<Terms />} />
        <Route path="/privacy" element={<PrivacyPolicy />} />
        <Route path="/oauth/callback" element={<OAuthCallback />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
