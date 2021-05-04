# TODO: Move here static definitions related ONLY to finra source
source = "FINRA_SHORTS"
filename_appendix = "FINRA_SV"

friendly_name = "FINRA Short reports"
description = """
Short volume reports from FINRA, reported daily.

Data contains {total volume:cyan}, {short volume:cyan} and {exempted volume:cyan},
which is short that is short volume that is exempted from the {uptick rule:bold} regulation.

FINRA posts data {no later than 6PM ET:cyan} of the same day
{NOTE:red|bold}
In rare instances, FINRA may need to update a file on a subsequent day.

When choosing to output one file per ticker the {symbol:cyan} will be removed
from the data to avoid redundancies.
"""  # noqa
