import numpy as np
import csv
import pandas as pd
from prince import CA, MCA

embedding_file = '' #Path of file that contains the crosstab that should be embedded

x = pd.read_csv(embedding_file)
x = x.set_index('user')

ca = CA(
    n_components=30,
    n_iter=10,
    copy=True,
    check_input=True,
    engine='sklearn',
    random_state=42
)

ca = ca.fit(x)

# basic stats
df = ca.eigenvalues_summary 

df["% of variance"] = df["% of variance"].str.replace('%','')
df["% of variance"] = df["% of variance"].astype(float)

df["% of variance"].plot()

#Export column coordinates
column_coord_file = '' #path to file column coordinates (e.g. party accounts or MPs) are exported to

column_coordinates = ca.column_coordinates(x)

column_coordinates.to_csv(column_coord_file)

#Export row coordinates
row_coord_file = '' #path to file row coordinates (e.g. followers of MPs) are exported to

row_coordinates = ca.row_coordinates(x)

row_coordinates.to_csv(row_coord_file)

