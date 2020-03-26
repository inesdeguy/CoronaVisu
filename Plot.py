import GetData
import plotly.express as px
from plotly.offline import plot
import pandas as pd

COL_REGION = 'Country/Region'

df_cases_world = GetData.get_frame('confirmed')
df_cases_world_group = df_cases_world.groupby(COL_REGION).sum()
df_cases_world_group.drop(['Lat', 'Long'], axis = 1, inplace = True)
df_cases_world_group.reset_index(inplace = True)
df_cases_world_group.rename(columns={COL_REGION:'country'}, inplace = True)

df_tmp = px.data.gapminder().query("year==2007")
df_tmp.drop(['year', 'lifeExp', 'pop', 'gdpPercap', 'iso_num'], axis = 1, inplace = True)

df_final = df_cases_world_group.merge(df_tmp, on = 'country')
lst=[]
for pays in df_final.country.unique():
    for col in df_final.columns[1:-2]:
        nb =df_final.set_index('country')[col][pays]
        continent = df_final.set_index('country')['continent'][pays]
        iso = df_final.set_index('country')['iso_alpha'][pays]
        lst+= [(pays,col,nb,continent,iso)]
df_ = pd.DataFrame(lst,columns=['Country','Date','Nombre','continent','iso_alpha'])
#fig = px.scatter_geo(df_final, locations="iso_alpha", color="continent",
#                     hover_name="country", size="Confirmed",
#                     projection="natural earth")
#plot(fig)

