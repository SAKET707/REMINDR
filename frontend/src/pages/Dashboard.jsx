import AppLayout from "../layouts/AppLayout";
import TelegramBanner from "../components/dashboard/TelegramBanner";
import ReminderCard from "../components/dashboard/ReminderCard";
import { useAuth } from "../context/useAuth";
import { useReminder } from "../context/useReminder";

export default function Dashboard() {
  const { user, loading: authLoading } = useAuth();
  const { reminders, loading: remindersLoading } = useReminder();

  if (authLoading || remindersLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background-soft">
        <h1 className="font-heading text-3xl font-bold text-primary-dark sm:text-4xl">
          Loading...
        </h1>
      </div>
    );
  }

  return (
    <AppLayout>
      {/* Hero */}

      <section>
        <h1 className="font-heading text-4xl font-bold leading-tight text-primary-dark sm:text-5xl lg:text-6xl xl:text-7xl">
          Dashboard
        </h1>

        <p className="mt-3 text-base leading-7 text-text-secondary sm:text-lg md:text-xl lg:text-2xl">
          Welcome back,{" "}
          <span className="font-semibold text-primary-dark">{user?.name}</span>.
        </p>
      </section>

      {/* Telegram Banner */}

      {!user?.telegram_chat_id && (
        <section className="mt-8 sm:mt-10">
          <TelegramBanner />
        </section>
      )}

      {/* Reminders */}

      <section className="mt-10 sm:mt-12">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="font-heading text-2xl font-semibold text-primary-dark sm:text-3xl lg:text-4xl">
            Upcoming Reminders
          </h2>
        </div>

        <div className="space-y-5">
          {reminders.length === 0 ? (
            <div className="rounded-2xl border border-border bg-card p-8 text-center shadow-sm">
              <p className="text-base text-text-secondary sm:text-lg">
                No upcoming reminders.
              </p>
            </div>
          ) : (
            reminders.map((reminder) => (
              <ReminderCard key={reminder.id} reminder={reminder} />
            ))
          )}
        </div>
      </section>
    </AppLayout>
  );
}
