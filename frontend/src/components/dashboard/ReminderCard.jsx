export default function ReminderCard({ reminder }) {
  return (
    <div className="rounded-2xl border border-border bg-white p-5 shadow-sm transition-shadow duration-300 hover:shadow-md sm:p-6 lg:p-8">
      <h3 className="font-heading text-lg font-semibold leading-snug text-primary-dark sm:text-xl lg:text-2xl">
        {reminder.email.subject}
      </h3>

      <p className="mt-3 text-sm leading-7 text-text-secondary sm:text-base lg:text-lg">
        {reminder.email.summary}
      </p>

      <p className="mt-5 text-sm font-medium text-primary sm:text-base lg:text-lg">
        {new Date(reminder.scheduled_for).toLocaleString()}
      </p>
    </div>
  );
}
