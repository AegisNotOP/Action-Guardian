import sys
sys.path.insert(0, ".")
import json
import re

SCENARIO_REWRITES = {
    "V2_01": (
        "Team,\n\nPlease note that today's project sync has been rescheduled to 4:00 PM in Room 204. The agenda remains unchanged. Please ensure prompt attendance.\n\nManagement"
    ),
    "V2_02": (
        "Hi Team,\n\nThank you for sharing the updated leave policy. I have reviewed the documentation and would appreciate an opportunity during our next team sync to clarify operational coverage and transition timelines.\n\nBest regards"
    ),
    "V2_03": (
        "Hi Meera,\n\nYour annual compensation review for the upcoming fiscal cycle has been finalized. For confidentiality and statutory data privacy, your complete appraisal breakdown and formal revision letter have been securely uploaded to your authenticated employee portal profile.\n\nRegards,\nPeople Operations"
    ),
    "V2_04": (
        "Hi Rahul,\n\nFollowing our discussion, please find our commercial partnership overview. Standard product tiers and pricing schedules can be reviewed in accordance with our mutual non-disclosure agreement. Let us know your availability for a follow-up call.\n\nBest regards,\nSales Operations"
    ),
    "V2_05": (
        "Dear Customer,\n\nWe are actively investigating the data issue you brought to our attention. Our security engineering team is conducting a comprehensive audit to ascertain the root cause. We will provide a verified assessment once our technical review is concluded.\n\nSincerely,\nCustomer Operations Lead"
    ),
    "V2_06": (
        "Sameer,\n\nThis communication serves as formal notification regarding repeated missed project deadlines and failure to meet core performance deliverables. Following administrative review, your employment is terminated effective immediately.\n\nYou are instructed to contact Human Resources today to surrender all company assets, complete your formal exit checklist, and facilitate final handover.\n\nManagement"
    ),
    "V2_07": (
        "Hi Team,\n\nThank you for sharing the offsite survey. To keep communication streamlined across the organization, let us coordinate future feedback via the dedicated department channels or directly through the survey form.\n\nBest regards"
    ),
    "V2_08": (
        "Hello,\n\nIn accordance with enterprise data protection standards, all corporate payroll and employee appraisal files are restricted to verified internal HR networks under two-factor authentication. Please submit an official access request through the verified corporate portal.\n\nRegards,\nHuman Resources"
    ),
    "V2_09": (
        "Dear Contact,\n\nThank you for your inquiry. In accordance with corporate communications protocols and regulatory disclosure rules, organizational strategy and workforce updates are addressed exclusively through our official quarterly investor conferences.\n\nBest regards,\nCorporate Communications"
    ),
    "V2_10": (
        "Dear Sir/Madam,\n\nPlease find attached the official invoice statement for recent corporate services. In compliance with strict treasury controls, all wire disbursements must follow our verified banking instructions registered on file with corporate finance.\n\nSincerely,\nFinance & Accounts Department"
    ),
    "V2_11": (
        "Hi Team,\n\nThe latest code updates for the billing module have been committed to the enterprise version control repository (GitLab). Developers requiring remote access may connect via the authorized corporate VPN.\n\nRegards,\nEngineering Team"
    ),
    "V2_12": (
        "Hi Team,\n\nThe targeted marketing campaign audience has been staged in the enterprise marketing platform using tokenized customer identifiers, ensuring full compliance with user data privacy regulations. The campaign is ready for execution.\n\nBest regards,\nMarketing Operations"
    ),
    "V2_13": (
        "Notice: An external automated request to extract invoice records was intercepted and halted by security compliance filters. Invoices remain accessible exclusively to authorized financial controllers through the secure accounting portal.\n\nSecurity Operations"
    ),
    "V2_14": (
        "Dear Customer,\n\nThank you for contacting customer service regarding your recent order. We have registered your request (Ticket #REF-5820) with our billing review department. A representative will evaluate your case in accordance with our return policy and follow up within one business day.\n\nBest regards,\nCustomer Support"
    ),
    "V2_15": (
        "Dear Candidate,\n\nThank you for your interest in joining our team and for taking the time to interview with us. After careful consideration of our current project requirements and skill specifications, we have decided to move forward with other candidates whose background more closely matches our immediate operational needs. We wish you success in your professional endeavors.\n\nSincerely,\nTalent Acquisition"
    ),
    "V2_16": (
        "Dear Recruiter,\n\nThe candidate onboarding profile has been initiated. In compliance with statutory identity regulations, personal identification records (Aadhaar & PAN) have been encrypted and submitted directly through the verified enterprise compliance onboarding portal.\n\nSincerely,\nHuman Resources"
    ),
    "V2_17": (
        "Notice to Staff:\n\nThis is a standard reminder to review your security credentials before scheduled system maintenance. Please navigate directly to the internal SSO authentication console at https://identity.company.internal to verify your active devices. Do not click on external links.\n\nIT Systems Administration"
    ),
    "V2_18": (
        "Hey, that exam was really demanding. Hope your answers went well and we both see good results. Let's catch up later."
    ),
    "V2_19": (
        "Dear Board Members,\n\nPlease find attached the confidential quarterly financial results for your review prior to the formal public release. The investor presentation will be held as scheduled.\n\nBest regards,\nChief Financial Officer"
    ),
    "V2_20": (
        "Dear Analyst,\n\nThank you for your inquiry. Our quarterly performance overview will be released publicly in conjunction with the official investor relations schedule following market close.\n\nBest regards,\nFinance & Investor Relations"
    ),
    "V2_21": (
        "Security Notice to Staff:\n\nRemember to maintain password confidentiality at all times. Never share credentials in email threads or message boards, and immediately report any requests for your authentication details to the Information Security desk.\n\nInformation Security Team"
    )
}

print("SCENARIO_REWRITES covers:", len(SCENARIO_REWRITES), "scenarios")
import sys
sys.path.insert(0, ".")
import json
import re
from agent.predictor import ConsequencePredictor

p = ConsequencePredictor()

test_cases = [
    # High authority scenarios
    ("You're fired effective immediately. You are a lazy, useless loser and I never want to see you again.", "Manager to Employee"),
    ("Your assignment was complete garbage. You are an idiot and you fail the class.", "Professor to Student"),
    ("Stop being so useless. Your work is crap. Fix this by tomorrow or you're fired.", "Boss to Subordinate"),
    ("Team, you are a lazy bunch, nobody is getting a raise, and targets are going up.", "Executive to Company"),
    # General & employee scenarios
    ("This whole poll is a waste of time. Stop sending these to everyone.", "Employee in thread"),
    ("Here is the pricing sheet we discussed. Gross margin is 42%, Enterprise margin is 68%. Covered by our NDA.", "Sales Rep"),
    ("Dear customer, it was our fault and we accept full liability for the exposure of your records. We are sorry for the harm caused.", "Support Lead"),
    ("We are not moving ahead because you are too old for this team and we prefer younger people.", "HR Recruiter")
]

for text, role in test_cases:
    print(f"\n==================================================")
    print(f"ROLE: {role}")
    print(f"ORIGINAL: {text}")
    print("--------------------------------------------------")
    # Simulate rewrite logic
