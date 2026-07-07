export default function TelegramBanner() {
  return (
    <div className="rounded-2xl border border-warning/30 bg-warning/10 p-6">
      <h3 className="font-heading text-2xl font-semibold text-primary-dark">
        Telegram not connected
      </h3>

      <p className="mt-2 text-lg text-text-secondary">
        Connect your Telegram account from the Profile page to receive reminder
        notifications.
      </p>
    </div>
  );
}
