import csv
import numpy as np
import pandas as pd
import scipy

# rotation function
def rotate_position(column1, column2, degree):
    rad = np.radians(degree)
    x = np.asarray(column1)
    y = np.asarray(column2)
    new_x = x * np.cos(rad) - y * np.sin(rad)
    new_y = x * np.sin(rad) + y * np.cos(rad)
    return new_x, new_y

# load MP embeddings and average per party
mp_embedding = './data/mp_embedding_pseudo_before_rotation.csv'
mp_df = pd.read_csv(mp_embedding)
mp_df = mp_df[mp_df['party'] != 'SSW'] 

party_coordinates = (
    mp_df.groupby('party')[['0', '2']]
    .mean()
    .reset_index()
)

# load CHES data; needs to be saved in data folder beforhand
df = pd.read_csv('./data/CHES2019V3.csv')
df = df[df['country'] == 3]
df = df.loc[:27]
df = df.replace(['GRUNEN', 'LINKE'], ['Bündnis 90/Die Grünen', 'DIE LINKE'])

# leave out non-informative dimensions
issues = list(df.columns)[4:]
throw_out = ['_require', '_sd', 'salience', '_blur']

dimensions = [
    el for el in issues
    if not any(term in el for term in throw_out)
]

df = df.drop(columns=['country', 'eastwest', 'party_id'])

# merge CHES with party coordinates
y = df.set_index('party').merge(party_coordinates.set_index('party'), on='party').reset_index()

# calculate optimal rotation per dimension
dimensions_degrees = []
dimensions_ycorr = []
dimensions_lrcorr = []

for el in dimensions:
    max_corr_dim_x = 0
    max_corr_dim_y = 0
    angle_dim = 0

    for deg in range(360):
        rot_x, rot_y = rotate_position(y['0'], y['2'], deg)

        pear_x = scipy.stats.pearsonr(rot_x, y['lrgen'])[0]
        pear_y = scipy.stats.pearsonr(rot_y, y[el])[0]

        abs_pear_x = abs(pear_x)
        abs_pear_y = abs(pear_y)

        if abs_pear_x + abs_pear_y > max_corr_dim_x + max_corr_dim_y:
            max_corr_dim_x = abs_pear_x
            max_corr_dim_y = abs_pear_y

            if pear_y < 0:
                angle_dim = (deg - 180) % 360
            else:
                angle_dim = deg

    dimensions_degrees.append(angle_dim)
    dimensions_ycorr.append(max_corr_dim_y)
    dimensions_lrcorr.append(max_corr_dim_x)

# overview table
overview = pd.DataFrame({
    'issue': dimensions,
    'rotation': dimensions_degrees,
    'ycorr': dimensions_ycorr,
    'lrcorr': dimensions_lrcorr
})

overview['overall_corr'] = overview['ycorr'] + overview['lrcorr']
overview = overview.sort_values('overall_corr', ascending=False)

# prepare final ordered issues and angles
issues = list(overview.issue)
angles = list(overview.rotation)

corr_angles = [
    el - 180 if el > 180 else el
    for el in angles
]

# determine final rotation angle
final_angle = 0

for idx, issue in enumerate(issues):
    issue_angle = corr_angles[idx]
    possible_mean = np.mean(corr_angles[:idx+1])

    rot_x, rot_y = rotate_position(y['0'], y['2'], possible_mean)

    pear_x = scipy.stats.pearsonr(rot_x, y['lrgen'])[0]
    if abs(pear_x) <= 0.8:
        break

    for iss in issues[:idx+1]:
        pear_y = scipy.stats.pearsonr(rot_y, y[iss])[0]

        if pear_y < -0.8:
            pear_y = scipy.stats.pearsonr(rot_y, -y[iss])[0]

        if pear_y < 0.8:
            print('Broken on dimension:', issue)
            print('Because of dimension:', iss)
            prev_angle = np.mean(corr_angles[:idx])
            print('Rotation angle before:', prev_angle)

            for iss in issues[:idx+1]:
                pear_y = scipy.stats.pearsonr(rot_y, y[iss])[0]
                print(f"{iss} correlation: {pear_y}")

            final_angle = prev_angle
            break

    if pear_y < 0.8:
        break

# rotate party coordinates using final angle
new_0, new_2 = rotate_position(
    list(party_coordinates['0']),
    list(party_coordinates['2']),
    final_angle + 180 # space then easier to interpret (ex-post decision)
)

party_coordinates_rotated = pd.DataFrame({
    'party': party_coordinates['party'],
    '0': new_0,
    '2': [-x for x in new_2]
})

# combine CDU/CSU for embedding
cducsu = (
    party_coordinates_rotated[
        party_coordinates_rotated['party'].isin(['CDU', 'CSU'])
    ][['0', '2']].mean()
)

party_coordinates_rotated = party_coordinates_rotated[
    ~party_coordinates_rotated['party'].isin(['CDU', 'CSU'])
]

party_coordinates_rotated = pd.concat([
    party_coordinates_rotated,
    pd.DataFrame([{
        'party': 'CDU/CSU',
        '0': cducsu['0'],
        '2': cducsu['2']
    }])
], ignore_index=True)

# color mapping
colmap = {
    'FDP': 'yellow',
    'Bündnis 90/Die Grünen': 'green',
    'AfD': 'blue',
    'DIE LINKE': 'deeppink',
    'CDU': 'black',
    'CSU': 'black',
    'SPD': 'red',
    'SSW': 'grey',
    'CDU/CSU': 'black'
}

party_coordinates_rotated['color'] = party_coordinates_rotated['party'].map(colmap)

# save result
party_coordinates_rotated.to_csv('party_pos_FINAL_2.csv', index=None)

# apply rotation to user_embedding
user_embedding = './data/embedding_pseudo_before_rotation.csv'
user_df = pd.read_csv(user_embedding)

new_0, new_2 = rotate_position(list(user_df['0']), list(user_df['2']), final_angle + 180)
user_df_rotated = pd.DataFrame({
    'user': user_df['user'],
    '0': new_0,
    '2': [-x for x in new_2] # mirror it on the y-axis.
})
user_df_rotated.to_csv('./data/embedding_pseudo_2.csv', index = None)
