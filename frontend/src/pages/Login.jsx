import { FcGoogle } from "react-icons/fc";
import { useNavigate } from "react-router-dom";
import { API_BASE_URL } from "../services/api";
import LeavesBg from "../assets/leaves-bg.jpg";

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
    <main className="relative flex min-h-screen overflow-hidden bg-primary-dark px-4 py-8 sm:px-6 sm:py-10 lg:px-12 lg:py-14 xl:px-20 2xl:px-32">
      {/* Background Image */}

      <img
        src={LeavesBg}
        alt=""
        aria-hidden="true"
        className="absolute inset-0 h-full w-full scale-105 object-cover opacity-80 blur-sm select-none pointer-events-none"
      />

      {/* Emerald Overlay */}

      <div className="absolute inset-0 bg-primary-dark/65"></div>

      <div className="relative z-10 mx-auto w-full max-w-5xl rounded-3xl border border-primary-dark/20 bg-background-soft/95 p-6 shadow-2xl backdrop-blur-md transition-shadow duration-300 sm:p-8 md:p-10 lg:p-12">
        {/* ================= HERO ================= */}

        <section className="text-center">
          {/* Brand */}

          <p className="inline-flex items-center rounded-full border border-primary-light/40 bg-primary-light/10 px-4 py-2 text-sm font-semibold uppercase tracking-[0.25em] text-primary-dark">
            REMINDR
          </p>

          {/* Accent */}

          <div className="mx-auto mt-6 h-1 w-20 rounded-full bg-primary-light"></div>

          {/* Heading */}

          <h1 className="mt-6 font-heading text-3xl font-bold leading-tight text-primary-dark sm:text-4xl md:text-5xl lg:text-6xl">
            Never miss an
            <br />
            important email.
          </h1>

          {/* Description */}

          <p className="mx-auto mt-5 max-w-3xl text-sm leading-7 text-text-secondary sm:text-base md:text-lg">
            AI-powered Gmail productivity assistant that intelligently
            identifies important emails, generates concise summaries, extracts
            deadlines, and reminds you before they're due.
          </p>
        </section>

        {/* Divider */}

        <hr className="mt-10 border-gray-300" />

        {/* ================= SIGN IN ================= */}

        <section className="mt-12">
          <div className="rounded-3xl border border-border bg-card p-5 text-center shadow-xl sm:p-6 lg:p-8">
            <h2 className="font-heading text-2xl font-bold text-primary-dark">
              Get Started
            </h2>

            <p className="mx-auto mt-3 max-w-xl text-base leading-7 text-text-secondary">
              Sign in with your Google account to securely connect your Gmail
              and let REMINDR start organizing your important emails.
            </p>

            {/* Google Button */}

            <button
              onClick={handleGoogleLogin}
              className="mt-8 flex w-full items-center justify-center gap-3 rounded-xl border border-gray-300 bg-white px-5 py-3 text-base font-semibold transition-all duration-300 hover:-translate-y-1 hover:border-primary hover:shadow-lg sm:gap-4 sm:px-6 sm:py-4 sm:text-lg"
            >
              <FcGoogle className="h-7 w-7 shrink-0" />
              Continue with Google
            </button>

            {/* Trust Text */}

            <p className="mt-6 text-sm leading-7 text-text-secondary">
              Secure Google OAuth login with{" "}
              <strong>read-only Gmail access</strong>. REMINDR never sends,
              edits, or deletes your emails.
            </p>

            <p className="mt-4 text-sm leading-7 text-text-secondary">
              By continuing, you agree to our{" "}
              <button
                onClick={handleTerms}
                className="font-medium text-primary-dark underline underline-offset-4 hover:text-primary"
              >
                Terms & Conditions
              </button>{" "}
              and{" "}
              <button
                onClick={handlePrivacy}
                className="font-medium text-primary-dark underline underline-offset-4 hover:text-primary"
              >
                Privacy Policy
              </button>
              .
            </p>
          </div>
        </section>

        {/* About REMINDR */}

        <section className="mt-14 rounded-3xl border border-border bg-card p-5 shadow-sm sm:p-6 lg:p-8">
          <h2 className="font-heading text-xl font-semibold text-primary-dark">
            About REMINDR
          </h2>

          <p className="mt-4 text-base leading-8 text-text-secondary">
            REMINDR is an AI-powered Gmail productivity assistant that helps you
            stay on top of important emails. After you sign in with Google,
            REMINDR securely accesses your Gmail using{" "}
            <strong>read-only</strong> permission to identify important emails,
            generate AI summaries, extract deadlines, and send timely reminders
            before deadlines arrive.
          </p>

          <p className="mt-4 text-base leading-8 text-text-secondary">
            REMINDR <strong>never sends, modifies, or deletes</strong> your
            Gmail messages. Your Google account remains under your control at
            all times.
          </p>
        </section>

        {/* ================= KEY FEATURES ================= */}

        <section className="mt-14">
          <div className="text-center">
            <h2 className="font-heading text-2xl font-bold text-primary-dark md:text-3xl">
              Why you'll love REMINDR
            </h2>

            <p className="mt-3 text-base text-text-secondary">
              Everything you need to stay on top of important emails.
            </p>
          </div>

          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:gap-6">
            {/* Card 1 */}

            <div className="rounded-2xl border border-border bg-card p-5 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-lg sm:p-6">
              <h3 className="font-heading text-base font-semibold text-primary-dark sm:text-lg">
                AI Email Summaries
              </h3>

              <p className="mt-2 text-sm leading-6 text-text-secondary sm:leading-7">
                Quickly understand lengthy emails with concise AI-generated
                summaries.
              </p>
            </div>

            {/* Card 2 */}

            <div className="rounded-2xl border border-border bg-card p-5 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-lg sm:p-6">
              <h3 className="font-heading text-base font-semibold text-primary-dark sm:text-lg">
                Deadline Detection
              </h3>

              <p className="mt-2 text-sm leading-6 text-text-secondary sm:leading-7">
                Automatically identifies due dates and important deadlines from
                your Gmail.
              </p>
            </div>

            {/* Card 3 */}

            <div className="rounded-2xl border border-border bg-card p-5 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-lg sm:p-6">
              <h3 className="font-heading text-base font-semibold text-primary-dark sm:text-lg">
                Smart Reminders
              </h3>

              <p className="mt-2 text-sm leading-6 text-text-secondary sm:leading-7">
                Receive timely reminders before deadlines so nothing slips
                through the cracks.
              </p>
            </div>

            {/* Card 4 */}

            <div className="rounded-2xl border border-border bg-card p-5 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-lg sm:p-6">
              <h3 className="font-heading text-base font-semibold text-primary-dark sm:text-lg">
                Secure Gmail Access
              </h3>

              <p className="mt-2 text-sm leading-6 text-text-secondary sm:leading-7">
                Uses Google's read-only permission. REMINDR never sends, edits,
                or deletes your emails.
              </p>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
