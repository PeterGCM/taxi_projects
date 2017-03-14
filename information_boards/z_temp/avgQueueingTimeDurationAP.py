import __init__
#
from information_boards import productivity_summary_fpath
#

import pandas as pd

df = pd.read_csv(productivity_summary_fpath)

print df['apAvgQueueing'].mean()
print df['apAvgDuration'].mean()