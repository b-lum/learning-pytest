from dateutil import parser
import re

print(parser.parse("5 days before December 1st, 2025", fuzzy=True).date())

print(
    re.findall(
        r"(\d+)\s+(days|weeks|months|years)", "1 year and 2 months after yesterday"
    )
)


print(
    re.findall(
        r"(\d+)\s+(days|weeks|months|years)", "1 year and 2 months after yesterday"
    )
)
print(
    re.findall(
        r"(\d+)\s+(days|weeks|months|years|year|month|week|day)",
        "1 year and 2 months after yesterday",
    )
)
