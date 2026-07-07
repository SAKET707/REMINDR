import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";

export default function OAuthCallback() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  useEffect(() => {
    const token = searchParams.get("token");

    if (!token) {
      navigate("/");
      return;
    }

    localStorage.setItem("access_token", token);

    navigate("/dashboard");
  }, [navigate, searchParams]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-background-soft">
      <p className="text-2xl font-semibold text-primary-dark">
        Signing you in...
      </p>
    </div>
  );
}
