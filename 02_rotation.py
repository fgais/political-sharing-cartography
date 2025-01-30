import csv
import numpy as np
import pandas as pd
import scipy

def rotate_position(column1, column2, degree):
    rad = np.radians(degree)
    li1 = list(column1)
    li2 = list(column2)
    for idx, el in enumerate(li1):
        li1[idx] = el*np.cos(rad) - li2[idx]*np.sin(rad)
        li2[idx] = el*np.sin(rad) + li2[idx]*np.cos(rad)
    return li1, li2

CHES_file = '' #path to CHES file
country_code = 3 #Germany
party_embedding = '' #Path to party embedding; name should match party name in CHES

df = pd.read_csv(CHES_file) 
df = df[df['country'] == country_code] 

throw_out = ['_require', '_sd', 'salience', '_blur'] #entries that do not refer to a party issue position
df = df.loc[:, ~df.columns.str.contains('|'.join(throw_out))]
df = df.drop(columns = ['country', 'eastwest', 'party_id']) #other entries

dimensions = df.columns[1:]

party_coordinates = pd.read_csv(party_embedding, dtype = str) 

dim1 = input('Name the first dimension (column name) of your embedding that you want to compare to CHES: ')
dim2 = input('Name the second dimension (column name) of your embedding that you want to compare to CHES: ')

party_coordinates[dim1] = party_coordinates[dim1].astype(float)
party_coordinates[dim2] = party_coordinates[dim2].astype(float)
party_coordinates = party_coordinates[['party', dim1, dim2]]

combined_df = df.set_index('party').merge(party_coordinates.set_index('party'), on='party') 
combined_df = combined_df.reset_index()

### Calculate max. correlation and angle for each dimension combined with left-right dimension

dimensions_degrees = []
dimensions_ycorr = []
dimensions_lrcorr = []

for el in dimensions:
    max_corr_dim_x = 0
    max_corr_dim_y = 0
    angle_dim = 0
    degs = np.arange(0, 360, 1)

    for deg in degs:
        rot_x = rotate_position(combined_df[dim1], combined_df[dim2], deg)[0]
        rot_y = rotate_position(combined_df[dim1], combined_df[dim2], deg)[1]

        pear_x = scipy.stats.pearsonr(rot_x, combined_df['lrgen'])[0]#abs(scipy.stats.pearsonr(rot_x, y['lrgen'])[0])
        pear_y = scipy.stats.pearsonr(rot_y, combined_df[el])[0]#abs(scipy.stats.pearsonr(rot_y, y[el])[0])
        abs_pear_x = abs(pear_x)
        abs_pear_y = abs(pear_y)
        
        if abs_pear_x + abs_pear_y > max_corr_dim_x + max_corr_dim_y:
            max_corr_dim_x = abs_pear_x
            max_corr_dim_y = abs_pear_y
            if pear_y < 0:
                angle_dim = deg-180
                if angle_dim < 0:
                    angle_dim = 360 + angle_dim
            else:
                angle_dim = deg
    dimensions_degrees.append(angle_dim)
    dimensions_ycorr.append(max_corr_dim_y)
    dimensions_lrcorr.append(max_corr_dim_x)

overview = pd.DataFrame(
    {'issue': dimensions,
     'rotation': dimensions_degrees,
     'ycorr': dimensions_ycorr,
     'lrcorr': dimensions_lrcorr
    })

overview = overview.set_index('issue')
overview['overall_corr'] = overview['ycorr'] + overview['lrcorr']
overview = overview.reset_index()
overview = overview.sort_values('overall_corr', ascending = False)

for idx, issue in enumerate(issues):
    issue_angle = corr_angles[idx]
    possible_mean = np.mean(corr_angles[:idx+1])

    rot_x = rotate_position(y['0'], y['2'], possible_mean)[0]
    rot_y = rotate_position(y['0'], y['2'], possible_mean)[1]
    final_angle = 0
    pear_x = scipy.stats.pearsonr(rot_x, y['lrgen'])[0]
    if abs(pear_x) < .8:
        print('Broken on dimension: ' + str(issue))
        print('Because of dimension: lrgen, correlation ' + str(pear_x))
        prev_angle = np.mean(corr_angles[:idx])
        print('Angle before: ' + str(prev_angle))
        final_angle = prev_angle
        break
    for iss in issues[:idx+1]:            
        pear_y = scipy.stats.pearsonr(rot_y, y[iss])[0]#abs(scipy.stats.pearsonr(rot_y, y[el])[0])
        if pear_y < -.8:
            pear_y = scipy.stats.pearsonr(rot_y, -y[iss])[0]
        if pear_y < .8:
            print('Broken on dimension: ' + str(issue))
            print('Because of dimension: ' + str(iss) + ', correlation ' + str(pear_y))
            prev_angle = np.mean(corr_angles[:idx])
            print('Angle before: ' + str(prev_angle))
            final_angle = prev_angle
            break

print('Correlations before: ')
final_rot_x = rotate_position(y['0'], y['2'], final_angle)[0]
final_rot_y = rotate_position(y['0'], y['2'], final_angle)[1]
print('lrgen correlation: ' + str(scipy.stats.pearsonr(rot_x, y['lrgen'])[0]))

for iss in issues[:idx]:
    pear_y = scipy.stats.pearsonr(final_rot_y, y[iss])[0]
    print(str(iss) + ' correlation: ' + str(pear_y))    
