source = "SEC_FTDS"
filename_appendix = "SEC_FTD"

friendly_name = "SEC FTDs"
description = """
Fail to deliver reports from SEC. Reported {twice a month:cyan}.

The relevant data is {the balance level outstanding:white|bold} recorded
by the NSCC CNS system.

{The values of total fails-to-deliver shares represent the aggregate:white|bold}
{net balance of shares that failed to be delivered as of a particular:white|bold}
{settlement date:white|bold}.

{Note:red}: for now date range will include the full month, so if you
request {2021/4/20 -> 2021/5/5:cyan} the generated data will contain
{everything:underline} for April and May.

If you choose to output {one file per ticker:cyan} the data will be
stripped of the {symbol:cyan} and {company:cyan} info, otherwise it will
contain everything found in the source data.
"""  # noqa
