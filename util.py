# Create directory to save output to
import os

base_dir = os.getcwd()

def export_soln_to_csv(df, model_name = 'untitled'):
    """ model refers to model object from docplex.mp.model"""

    try:
        os.mkdir(os.path.join(base_dir, 'output'))
    except:
        pass

    filename = 'output/' + 'soln_' + model_name + '.csv'
    solution_output = os.path.join(os.getcwd(), filename)
    df.to_csv(solution_output, index=False)


# ****************************************
# check
# ****************************************
from docplex.mp.model import Model
import pandas as pd

# sample df
d = {'col1': [1, 2], 'col2': [3, 4]}
df = pd.DataFrame(data=d)

# sample model
m = Model('9.3-1')

if __name__ == '__main__':
    export_soln_to_csv(df)
    # export_soln_to_csv(df, m.get_name())
