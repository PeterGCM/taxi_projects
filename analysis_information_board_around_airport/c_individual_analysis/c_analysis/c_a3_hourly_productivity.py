from __future__ import division
#
import os, sys
sys.path.append(os.getcwd() + '/../..')
#
from supports._setting import hourly_productivities
from supports._setting import TIME_SLOTS, SEC3600, CENT
from supports.charts import multiple_line_chart

import pandas as pd

productivities = pd.read_csv(hourly_productivities)

productivities['diff.'] = productivities.apply(lambda row: row['ap-productivity'] - row['ap-out-productivity'], axis=1)

xs = range(len(TIME_SLOTS))
yss = [
        [x * SEC3600 / CENT for x in productivities.groupby(['hh']).mean()['ap-productivity']],
        [x * SEC3600 / CENT for x in productivities.groupby(['hh']).mean()['ap-out-productivity']],
        [x * SEC3600 / CENT for x in productivities.groupby(['hh']).mean()['diff.']]       
       ]
#
multiple_line_chart((12, 6), '', 'Time slot', 'Unit 1,000',
                    (xs, 0), yss, ['ap-prod.', 'ap-out-prod.', 'diff.'], 'upper left', 'productivity')