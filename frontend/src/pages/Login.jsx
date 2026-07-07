import { FcGoogle } from "react-icons/fc";
import { useNavigate } from "react-router-dom";
import { API_BASE_URL } from "../services/api";

export default function Login() {
  const navigate = useNavigate();

  const handleGoogleLogin = () => {
    window.location.href = `${API_BASE_URL}/auth/google/login`;
  };

  const handleTerms = () => {
    navigate("/terms");
  };

  const handlePrivacy = () => {
    navigate("/privacy");
  };

  return (
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden bg-primary-dark px-6 lg:px-12 xl:px-20 2xl:px-32">
      <div className="relative z-10 w-full max-w-xl rounded-2xl border border-primary-dark bg-background-soft p-24 transition-shadow duration-300 hover:shadow-2xl lg:max-w-2xl xl:max-w-3xl">
        {/* Brand */}

        <p className="text-sm font-semibold uppercase tracking-[0.4em] text-primary-dark md:text-base">
          REMINDR
        </p>

        {/* Heading */}

        <h1 className="mt-5 font-heading text-5xl font-bold leading-[1.05] tracking-tight text-primary-dark sm:text-6xl lg:text-7xl xl:text-8xl">
          Never miss an important email.
        </h1>

        {/* Description */}

        <p className="mt-8 max-w-2xl text-lg leading-9 text-text-secondary md:text-xl xl:text-2xl">
          REMINDR intelligently filters your Gmail, summarizes important emails,
          extracts deadlines and reminds you before it's too late.
        </p>

        {/* Divider */}

        <hr className="mt-12 border-gray-300" />

        {/* Google Button */}

        <button
          onClick={handleGoogleLogin}
          className="mt-12 flex w-full items-center justify-center gap-4 rounded-2xl border-2 border-gray-300 bg-white px-8 py-5 text-lg font-semibold shadow-sm transition-all duration-300 hover:-translate-y-0.5 hover:border-primary hover:shadow-lg xl:py-6 xl:text-xl"
        >
          <FcGoogle className="h-8 w-8 shrink-0" />
          Continue with Google
        </button>

        {/* Trust Text */}

        <p className="mt-6 text-[15px] leading-7 text-text-secondary">
          Secure Google OAuth login with read-only Gmail access. By continuing,
          you agree to our{" "}
          <button
            onClick={handleTerms}
            className="cursor-pointer font-medium text-primary-dark underline underline-offset-4 hover:text-primary-light"
          >
            Terms
          </button>{" "}
          and{" "}
          <button
            onClick={handlePrivacy}
            className="cursor-pointer font-medium text-primary-dark underline underline-offset-4 hover:text-primary-light"
          >
            Privacy Policy
          </button>
          .
        </p>
      </div>
    </main>
  );
}
