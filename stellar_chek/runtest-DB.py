import roundcheck as rk
import numpy as np
import sqlalchemy as sa


thresholds = range(1, 50, 1)

run = lambda t: rk.go_test(rk.cat, rk.data, t)

tablename = 'results_table'
#connection = sa.create_engine('sqlite:////home/bos0109/sersic/work/rhino/src/rhino/stellar_check/sigma_results.db')
engine = sa.create_engine('sqlite:///sigma_results2.db')


for thresh in thresholds:
    dframe = run(thresh)
    dframe.to_sql(tablename, engine, if_exists='append')
    
