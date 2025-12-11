import requests
import hashlib
import time
from datetime import datetime

class BreachMonitor:
    def __init__(self):
        self.hibp_api = "https://haveibeenpwned.com/api/v3"
        self.headers = {
            'User-Agent': 'Python Breach Monitor',
            'hibp-api-key': 'YOUR_API_KEY_HERE'
        }

    def check_email_breach(self, email):

        print(f"\n🔍 Checking Your Email: {email}")
        print("=" * 60)

        try:

            url = f"{self.hibp_api}/breachedaccount/{email}?truncateResponse=false"
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                breaches = response.json()
                print(f"⚠️  WARNING: Your email {len(breaches)} data breaches!\n")

                for breach in breaches:
                    print(f"📌 Breach Name: {breach['Name']}")
                    print(f"   Date: {breach['BreachDate']}")
                    print(f"   Compromised Data: {', '.join(breach['DataClasses'])}")
                    print(f"   Description: {breach['Description'][:100]}...")
                    print(f"   Domain: {breach['Domain']}")
                    print("-" * 60)

                return breaches

            elif response.status_code == 404:
                print("✅ Good news! Your email is not show known breaches.")
                return []

            elif response.status_code == 401:
                print("❌ API key is required. Free API key  haveibeenpwned.com registered.")
                print("    Alternative: Manually check- https://haveibeenpwned.com/")
                return None

            else:
                print(f"⚠️  Error: Status code {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            print("💡 Solution: Check Internet connection and manually checking:")
            print("   https://haveibeenpwned.com/")
            return None

    def check_password_compromised(self, password):

        print(f"\n🔐 Password security checking...")
        print("=" * 60)

        try:
            #
            sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
            prefix = sha1_hash[:5]
            suffix = sha1_hash[5:]


            url = f"https://api.pwnedpasswords.com/range/{prefix}"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:

                hashes = response.text.split('\r\n')
                for hash_line in hashes:
                    hash_suffix, count = hash_line.split(':')
                    if hash_suffix == suffix:
                        print(f"⚠️  DANGER: This password {count} repeat data breaches shown!")
                        print("🚨 IMMEDIATE ACTION: This is a change password immediate!")
                        return int(count)

                print("✅ Good! This password known breaches not showing.")
                print("💡 But Use to strong and unique password use.")
                return 0

            else:
                print(f"⚠️  Error: Status code {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Error: {e}")
            return None

    def generate_security_report(self, email, check_password=False, password=None):

        print("\n" + "=" * 60)
        print("🛡️  DATA BREACH SECURITY REPORT")
        print("=" * 60)
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📧 Email: {email}")
        print("=" * 60)

        # Email check
        breaches = self.check_email_breach(email)

        # Password check (optional)
        if check_password and password:
            time.sleep(2)
            password_count = self.check_password_compromised(password)

        # Recommendations
        print("\n" + "=" * 60)
        print("📋 RECOMMENDATIONS - What you have to do:")
        print("=" * 60)

        if breaches and len(breaches) > 0:
            print("\n   HIGH PRIORITY ACTIONS:")
            print("1. ✓ Immediately email password change")
            print("2. ✓ Two-Factor Authentication (2FA) enable")
            print("3. ✓ Every linked accounts passwords change")
            print("4. ✓ Bank statements and credit card transactions monitoring")
            print("5. ✓ Raise a Cyber crime portal complaint file")
            print("   → https://cybercrime.gov.in")
        else:
            print("\n✅ PREVENTIVE ACTIONS:")
            print("1. ✓ Strong passwords use  (12+ characters)")
            print("2. ✓ every account is change a password use")
            print("3. ✓ Use to Password manager(Bitwarden, LastPass)")
            print("4. ✓ 2FA every place enable")
            print("5. ✓ Regular monitoring (Every 3 months)")

        print("\n ADDITIONAL RESOURCES:")
        print("• Have I Been Pwned: https://haveibeenpwned.com/")
        print("• India Cyber Crime: https://cybercrime.gov.in")
        print("• Helpline: 1930")
        print("=" * 60)

        # Save report to file
        self.save_report(email, breaches)

    def save_report(self, email, breaches):
        """
        Report to convert a text file
        """
        try:
            filename = f"breach_report_{email.replace('@', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"DATA BREACH REPORT\n")
                f.write(f"{'=' * 60}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Email: {email}\n")
                f.write(f"{'=' * 60}\n\n")

                if breaches and len(breaches) > 0:
                    f.write(f"Total Breaches Found: {len(breaches)}\n\n")
                    for breach in breaches:
                        f.write(f"Breach: {breach['Name']}\n")
                        f.write(f"Date: {breach['BreachDate']}\n")
                        f.write(f"Data: {', '.join(breach['DataClasses'])}\n")
                        f.write(f"{'-' * 60}\n")
                else:
                    f.write("No breaches found.\n")

            print(f"\n💾 Report saved: {filename}")

        except Exception as e:
            print(f"⚠️  Could not save report: {e}")

def main():

    print("""
    ╔══════════════════════════════════════════════════════╗
    ║           DATA BREACH MONITORING TOOL                ║
    ║                                                      ║
    ║  this tool you help to find data breach              ║
    ║  this not data remove - Only check                   ║
    ║  data and you help to monitering.                    ║
    ╚══════════════════════════════════════════════════════╝
    """)

    monitor = BreachMonitor()

    email = input("\n enter your email: ").strip()

    check_pwd = input(" Enter Your Password? (yes/no): ").strip().lower()
    password = None

    if check_pwd in ['yes', 'y', 'no',]:
        password = input("   Enter password (secure - does not show display your password): ").strip()
        print("[Password entered - checking...]")

    # Report generate
    monitor.generate_security_report(email, check_pwd in ['yes', 'y', 'no',], password)

    print("\n Scan complete!")
    print("\n IMPORTANT: If the breach, so action taken to important is compulsory!")

if __name__ == "__main__":
    main()