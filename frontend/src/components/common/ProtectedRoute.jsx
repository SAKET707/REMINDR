import { Navigate } from "react-router-dom";
import { useAuth } from "../../context/useAuth";

export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background-soft">
        <h1 className="font-heading text-4xl font-bold text-primary-dark">
          Loading...
        </h1>
      </div>
    );
  }

  const token = localStorage.getItem("access_token");

  if (!token || !user) {
    return <Navigate to="/" replace />;
  }

  return children;
}
