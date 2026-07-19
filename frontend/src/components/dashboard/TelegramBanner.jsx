export default function TelegramBanner() {
  return (
    <div className="rounded-2xl border border-warning/30 bg-warning/10 p-5 shadow-sm sm:p-6 lg:p-8">
      <h3 className="font-heading text-lg font-semibold text-primary-dark sm:text-xl lg:text-2xl">
        Telegram not connected
      </h3>

      <p className="mt-3 text-sm leading-7 text-text-secondary sm:text-base lg:text-lg">
        Connect your Telegram account from the Profile page to receive reminder
        notifications.
      </p>
    </div>
  );
}
