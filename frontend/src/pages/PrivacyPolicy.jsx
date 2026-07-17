import PolicyLayout from "../layouts/PolicyLayout";
import Section from "../components/common/Section";
import Divider from "../components/common/Divider";
import Highlight from "../components/common/Highlight";
import BulletList from "../components/common/BulletList";

export default function PrivacyPolicy() {
  return (
    <PolicyLayout
      title="Privacy Policy"
      subtitle="Your privacy matters to us. This Privacy Policy explains what information REMINDR collects, how it is used, and how we protect your data."
    >
      <Highlight>
        REMINDR only accesses your Gmail account with your permission and uses
        Gmail read-only access exclusively to analyze emails, generate
        reminders, and improve your productivity. We never send, modify, or
        delete your emails.
      </Highlight>

      <Divider />

      <Section title="1. Information We Collect">
        <p>When you use REMINDR, we may collect the following information:</p>

        <BulletList>
          <li>Google account name</li>
          <li>Email address</li>
          <li>Profile picture</li>
          <li>Email subject</li>
          <li>Email body</li>
          <li>Email received time</li>
          <li>AI-generated summaries</li>
          <li>Extracted deadlines and tasks</li>
          <li>Reminder information</li>
          <li>Telegram chat ID (if Telegram is connected)</li>
        </BulletList>
      </Section>

      <Divider />

      <Section title="2. How We Use Your Information">
        <p>
          The information collected is used only to provide REMINDR's core
          functionality.
        </p>

        <BulletList>
          <li>Analyze incoming Gmail messages.</li>
          <li>Identify actionable emails.</li>
          <li>Generate AI-powered summaries.</li>
          <li>Detect deadlines and important tasks.</li>
          <li>Schedule reminders automatically.</li>
          <li>Send dashboard and Telegram notifications.</li>
          <li>Improve application reliability and performance.</li>
        </BulletList>
      </Section>

      <Divider />

      <Section title="3. Google API Data">
        <p>
          REMINDR uses the Gmail API with read-only permissions to analyze your
          emails.
        </p>

        <p>The application can:</p>

        <BulletList>
          <li>Read email content.</li>
          <li>Extract tasks and deadlines.</li>
          <li>Create reminders based on detected information.</li>
        </BulletList>

        <p>The application will never:</p>

        <BulletList>
          <li>Send emails on your behalf.</li>
          <li>Modify Gmail messages.</li>
          <li>Delete Gmail messages.</li>
          <li>Mark emails as read.</li>
        </BulletList>

        <Highlight>
          REMINDR uses Google user data only to provide the features you
          request. We do not use Gmail data for advertising or sell it to third
          parties.
        </Highlight>
      </Section>

      <Divider />

      <Section title="4. Data Storage">
        <p>
          Processed email information, reminders, and account details are stored
          securely in our PostgreSQL database.
        </p>

        <BulletList>
          <li>OAuth refresh tokens are encrypted before storage.</li>
          <li>Authentication uses secure JWT tokens.</li>
          <li>
            Sensitive data is protected using industry-standard security
            practices.
          </li>
        </BulletList>
      </Section>

      <Divider />

      <Section title="5. Data Sharing">
        <p>We do not sell, rent, or trade your personal information.</p>

        <p>
          Your information is shared only when necessary to operate REMINDR.
        </p>

        <BulletList>
          <li>Google APIs (for Gmail access).</li>
          <li>AI model providers for email analysis.</li>
          <li>Telegram (only if you enable notifications).</li>
        </BulletList>
      </Section>

      <Divider />

      <Section title="6. Security">
        <p>We take reasonable measures to protect your information.</p>

        <BulletList>
          <li>Encrypted OAuth refresh tokens.</li>
          <li>JWT-based authenticated API access.</li>
          <li>Secure HTTPS communication when deployed.</li>
          <li>Restricted access to stored application data.</li>
        </BulletList>
      </Section>

      <Divider />

      <Section title="7. Your Rights & Control">
        <p>You remain in control of your data.</p>

        <BulletList>
          <li>Disconnect Telegram at any time.</li>
          <li>Delete your REMINDR account.</li>
          <li>Revoke Google account access.</li>
          <li>Revoke Gmail permissions from your Google Account.</li>
        </BulletList>
      </Section>

      <Divider />

      <Section title="8. Data Retention">
        <p>
          REMINDR retains only the information required to provide reminder
          functionality.
        </p>

        <p>
          When your account is deleted, associated application data is
          permanently removed, subject to any legal obligations that may require
          temporary retention.
        </p>
      </Section>

      <Divider />

      <Section title="9. Children's Privacy">
        <p>
          REMINDR is not intended for children under 13 years of age. We do not
          knowingly collect personal information from children.
        </p>
      </Section>

      <Divider />

      <Section title="10. Changes to This Privacy Policy">
        <p>
          We may update this Privacy Policy from time to time to reflect changes
          in our services, legal requirements, or security practices.
        </p>

        <p>
          Significant changes will be communicated through the application when
          appropriate.
        </p>
      </Section>

      <Divider />

      <Section title="11. Contact">
        <p>
          If you have any questions about these Terms, this Privacy Policy, or
          how your information is handled, please contact us at:
        </p>

        <div className="mt-4 rounded-xl border border-border bg-secondary-light p-5">
          <p className="font-semibold text-primary">
            Email : saketacad@gmail.com
          </p>
        </div>
      </Section>
    </PolicyLayout>
  );
}
