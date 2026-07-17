import PolicyLayout from "../layouts/PolicyLayout";
import Section from "../components/common/Section";
import Divider from "../components/common/Divider";
import Highlight from "../components/common/Highlight";
import BulletList from "../components/common/BulletList";

export default function Terms() {
  return (
    <PolicyLayout
      title="Terms & Conditions"
      subtitle="Please read these Terms and Conditions carefully before using REMINDR. By accessing or using the application, you agree to be bound by these terms."
    >
      <Highlight>
        REMINDR is an AI-powered productivity assistant. It is designed to help
        you manage important emails and reminders but should not be considered a
        substitute for your own judgment.
      </Highlight>

      <Divider />

      <Section title="1. Acceptance of Terms">
        <p>
          By accessing or using REMINDR, you acknowledge that you have read,
          understood, and agreed to these Terms & Conditions. If you do not
          agree with any part of these terms, please discontinue use of the
          application.
        </p>
      </Section>

      <Divider />

      <Section title="2. Google Account">
        <p>
          Access to REMINDR requires authentication using a valid Google
          account.
        </p>

        <p>You are responsible for:</p>

        <BulletList>
          <li>Maintaining the security of your Google account.</li>
          <li>Keeping your login credentials confidential.</li>
          <li>Any activity performed through your account.</li>
        </BulletList>
      </Section>

      <Divider />

      <Section title="3. Gmail Access">
        <p>
          REMINDR requests Gmail read-only permission solely to provide reminder
          and productivity features.
        </p>

        <p>The application uses Gmail access to:</p>

        <BulletList>
          <li>Read newly received emails.</li>
          <li>Identify actionable emails.</li>
          <li>Extract deadlines and important tasks.</li>
          <li>Generate AI-powered summaries.</li>
          <li>Create reminders.</li>
        </BulletList>

        <Highlight>
          REMINDR never sends emails, modifies emails, deletes emails, or marks
          emails as read.
        </Highlight>
      </Section>

      <Divider />

      <Section title="4. AI Analysis">
        <p>
          REMINDR uses artificial intelligence to analyze email content and
          generate summaries, detect deadlines, and identify actionable tasks.
        </p>

        <p>
          While we strive for high accuracy, AI-generated information may
          occasionally be incomplete or incorrect.
        </p>

        <p>
          Users remain solely responsible for verifying important dates,
          deadlines, and actions before relying on reminders.
        </p>
      </Section>

      <Divider />

      <Section title="5. Telegram Notifications">
        <p>
          Telegram notifications are completely optional and require explicit
          user consent.
        </p>

        <p>By connecting Telegram, you agree to receive:</p>

        <BulletList>
          <li>Reminder notifications.</li>
          <li>Upcoming deadline alerts.</li>
          <li>Task reminders generated from your emails.</li>
        </BulletList>

        <p>
          You may disconnect Telegram at any time from your profile settings.
        </p>
      </Section>

      <Divider />

      <Section title="6. User Responsibilities">
        <p>Users agree not to:</p>

        <BulletList>
          <li>Use REMINDR for unlawful purposes.</li>
          <li>Attempt unauthorized access to the service.</li>
          <li>Interfere with application security.</li>
          <li>Reverse engineer or exploit the platform.</li>
          <li>Abuse or overload the service.</li>
        </BulletList>
      </Section>

      <Divider />

      <Section title="7. Service Availability">
        <p>
          REMINDR is provided on a best-effort basis. Although we aim for high
          availability, uninterrupted service cannot be guaranteed.
        </p>

        <p>Reminder delivery may be affected by:</p>

        <BulletList>
          <li>Google Gmail API availability.</li>
          <li>Internet connectivity.</li>
          <li>Telegram outages.</li>
          <li>Cloud infrastructure issues.</li>
          <li>Scheduled maintenance.</li>
        </BulletList>
      </Section>

      <Divider />

      <Section title="8. Limitation of Liability">
        <p>REMINDR is intended solely as a productivity tool.</p>

        <p>We are not responsible for:</p>

        <BulletList>
          <li>Missed deadlines.</li>
          <li>Incorrect AI predictions.</li>
          <li>Delayed notifications.</li>
          <li>Losses resulting from reliance on reminders.</li>
          <li>Temporary service interruptions.</li>
        </BulletList>
      </Section>

      <Divider />

      <Section title="9. Account Deletion">
        <p>
          You may permanently delete your REMINDR account at any time through
          the application.
        </p>

        <p>
          Account deletion permanently removes your stored application data in
          accordance with our Privacy Policy.
        </p>
      </Section>

      <Divider />

      <Section title="10. Changes to These Terms">
        <p>
          We may revise these Terms & Conditions from time to time to reflect
          changes in our services, legal requirements, or security practices.
        </p>

        <p>
          Continued use of REMINDR after updates become effective constitutes
          acceptance of the revised Terms.
        </p>
      </Section>
    </PolicyLayout>
  );
}
