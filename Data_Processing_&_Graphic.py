import pandas as pd
import altair as alt

# The objective of this document is to prepare the following dataframe (you can find YourData.xls in the GitHub):
df = pd.read_excel(r'Insert_Your_Working_Directory\YourData.xls'
                   , sheet_name=0, usecols='A:Q', header=1, nrows=30)

# to create a correct visualization with Altair library, where we can comparise the Health of a list of surveyed people
# depending on the age and the sex. I proceed to explain the steps to obtain the adjoint graphic in the GitHub.

# 1) Process the data:

# rename the columns
mylist = ['Age', 'Health', 'Men_Est', 'Men_lim_inf', 'Men_lim_sup', 'Women_Est', 'Women_lim_inf', 'Women_lim_sup']
df.columns = mylist

# fill the gaps in the variable 'Age
age = df['Age']
for j in range(0, len(df)):
    if j % 6 != 0:
        df['Age'][j] = age[j - 1]

# Remove NA's
df = df.dropna()
df.index = range(0, len(df))

# Change '-' to 0
for col in df.columns:
    for k in range(0, len(df)):
        if df[col][k] == '-':
            df[col][k] = 0

# 2) Organize the data.
# I would like to create a graphic which segregates by Age and Sex.
# For this purpose, I need Sex to be a variable.
# Then I extract the information of the inferior and superior limit
lim_inf = []
lim_sup = []

for i in range(0, len(df)):
    lim_inf.append(df['Men_lim_inf'][i])
    lim_sup.append(df['Men_lim_sup'][i])

for i in range(0, len(df)):
    lim_inf.append(df['Women_lim_inf'][i])
    lim_sup.append(df['Women_lim_sup'][i])

df = df.drop(['Men_lim_inf', 'Men_lim_sup', 'Women_lim_inf', 'Women_lim_sup'],
             axis=1)

# and I melt the dataframe
df = df.melt(id_vars=['Age', 'Health'], var_name='M', value_name='Est')

# this means that, except for 'Age' and 'Health', the
# rest of the variables are now values of a new variable named 'M', and
# the values of the old variable are now in the new variable 'Est'

# Now recuperate the limits information
df['lim_inf'] = lim_inf
df['lim_sup'] = lim_sup

# and create the 'Sex' variable from 'M'
Sex = []
for k in range(0, len(df)):
    Sex.append(df['M'][k].replace('Men_Est', 'Men').replace('Women_Est', 'Women'))

df['Sex'] = Sex
df = df.drop('M', axis=1)

# 3) Aesthetics details

# Move 'Est', 'lim_inf' and 'lim_sup' to a 1-100 scale
est = []
inf = []
sup = []
for k in range(0, len(df)):
    est.append(round(df['Est'][k] * 100, 1))
    inf.append(round(df['lim_inf'][k] * 100, 1))
    sup.append(round(df['lim_sup'][k] * 100, 1))

df = df.drop(['Est', 'lim_inf', 'lim_sup'], axis=1)
df['Est'] = est
df['lim_inf'] = inf
df['lim_sup'] = sup


# Delete 'All ages' rows (I do not want them for the graphic)

df = df[df.Age!= 'All ages']
df.index = range(0,len(df)) # Always remember to reindex!

# Add 'years' to the values of 'Age'
age = []
for j in range(0, len(df)):
    age.append(df['Age'][j])

df.drop('Age', axis=1)

df['Age'] = age


# And create a new variable which indicates that
# all this values are for the Survey 1
df['M'] = 'Survey 1'

# 4) Visualization with altair

# To select the stacking order in the bar graph, I create a categorical
# order with the variable 'order'
cat_orden = ['Excellent', 'Very Good', 'Good', 'Regular', 'Bad']

df['order'] = df['Health'].replace({val: -i for i, val in enumerate(cat_orden)})


# Now we are in conditions to create the graphic
selection = alt.selection_multi(fields=['Health'], bind='legend')
# This selection will make the graphic interactive

bar_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('M:N', title=None, axis=alt.Axis(labelAngle=0)),
    y=alt.Y('Est:Q', title='Percentage Estimation'),
    color=alt.Color('Health:N', scale=alt.Scale(scheme='spectral', reverse=True),
                    # optional: make color order in legend match stack order
                    sort=alt.EncodingSortField('order', order='descending'),
                    legend=alt.Legend(title="", symbolSize=400, symbolType='square', labelLimit=0)),
    order='order',  # this controls stack order
    tooltip=[alt.Tooltip('Est', title='Estimation'), alt.Tooltip('lim_inf', title='Inferior Limit'), # this adds the hovering effect
             alt.Tooltip('lim_sup', title='Superior Limit')],
    opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
).add_selection(
    selection
).transform_filter(selection
                   ).properties(
    width=180,
    height=180
).facet(
    title='Health in the 1st survey with respect to Sex and Age group',
    row=alt.Row('Sex:N', title=None, header=alt.Header(labelFontSize=15)),
    column=alt.Column('Age:N', title=None, header=alt.Header(labelFontSize=15))
)

## scale = alt.Scale(range=['darkgreen', 'palegreen', 'khaki', 'lightcoral', 'firebrick'])

leyenda = alt.Chart(df).mark_text().encode(
    color=alt.Color('Health:N', scale=alt.Scale(scheme='spectral', reverse=True),
                    # optional: make color order in legend match stack order
                    sort=alt.EncodingSortField('order', order='descending'),
                    legend=alt.Legend(title="",
                                      symbolSize=400, symbolType='square', labelLimit=0, labelAlign='left',
                                      offset=-20)),
    opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
).add_selection(selection)

example_for_application = alt.hconcat(bar_chart, leyenda).configure_view(strokeWidth=0).configure_title(
    color='black',
    dy=-20,
    dx=70)

example_for_application.show()

# In this graphic, you may contrast the health among different groups of age and sex.
# You can see the specific details of the data by hovering on the bars. Moreover, if you click on
# the right hand side legend, the graphic transforms and you can see in more detail a specific
# kind of Health. In our case, we only have one survey, but the same can be done with four survey in the
# x axis, obtaining a total of 32 clearly distinguished bars in the same graphic, which proves itself
# quite useful at the time of exploring the data.

