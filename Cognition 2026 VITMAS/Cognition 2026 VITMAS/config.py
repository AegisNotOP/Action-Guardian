"""
ActionGuardian - Fixed SMTP Email Configuration
Configure your fixed sender email and App Password here once.
"""

# Presentation / Pitch Safety Mode
# When DEMO_MODE = True, ActionGuardian runs in safe Presentation Sandbox Mode:
# - Full RFC syntax and real DNS domain validations execute
# - Security audit receipt (rcpt_...) is generated and verified
# - Zero spam or unintended emails are sent over SMTP during live judge tests
# Set to False to enable live Gmail SMTP dispatch.
DEMO_MODE = True

# SMTP Server configuration (Default is Gmail)
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

# Your fixed Sender Email address
SENDER_EMAIL = "riskfinder101@gmail.com"

# Your fixed 16-character Google App Password (or SMTP password)
# (To generate a Gmail App Password: Google Account -> Security -> 2-Step Verification -> App Passwords)
SENDER_PASSWORD = "ljtj ubuv fkpa llsq"
