
# coding: utf-8

# In[ ]:


import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np
import plotly.graph_objs as go


# In[82]:


url='https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module4/Data/riverkeeper_data_2013.csv'
riverKeeper_df = pd.read_csv(url)


riverKeeper_df['EnteroCount'] = riverKeeper_df['EnteroCount'].str.replace('[^\w\s]','')
riverKeeper_df['EnteroCount']=riverKeeper_df['EnteroCount'].apply(pd.to_numeric, errors='coerce')
riverKeeper_df['Date'] = pd.Series([pd.to_datetime(d) for d in riverKeeper_df['Date']])

uniqueDate=riverKeeper_df['Date'].unique()
uniqueDate= pd.Series([pd.to_datetime(d) for d in uniqueDate])


# In[83]:


sites = riverKeeper_df.groupby(riverKeeper_df['Site'])["EnteroCount"].mean().reset_index()
sites = sites.sort_values('EnteroCount').reset_index(drop=True)


# In[84]:


def Graph(Title):
    site = sites.sort_values('EnteroCount',ascending=False)
    traces=go.Bar(
        x=site['EnteroCount'],
        y=site['Site'],
        orientation = 'h'
    )

    return {
        'data' : [traces], 
        'layout': go.Layout(
            width = 800,
            height = 500,
            title = Title,
            xaxis = dict(
                title = 'EnteroCount',
                titlefont=dict(
                    family='Arial, sans-serif',
                    size=18,
                    color='lightgrey'
                )
            ),
            yaxis = dict(
                title = 'Sites',
                titlefont=dict(
                    family='Arial, sans-serif',
                    size=18,
                    color='lightgrey'
                ),
                showticklabels=True,
                tickangle=45,
                tickfont=dict(
                    family='Old Standard TT, serif',
                    size=6,
                    color='black'
                )    
            )
        )
    }



# In[85]:


def PlotResult(df,Title,Color):
    if Color == "green":
        barColor='rgb(50,255,50)'
    else:
        barColor='rgb(255,0,0)'

    traces = go.Bar(
        x=df['EnteroCount'],
        y=df['Site'],
        orientation = 'h',
        marker=dict(
            color=barColor,
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        )
    )
    return {
            'data' : [traces], 
            'layout': go.Layout(
                width = 800,
                height = 500,
                title = Title,
                xaxis = dict(
                    title = 'EnteroCount',
                    titlefont=dict(
                        family='Arial, sans-serif',
                        size=18,
                        color='lightgrey'
                    )
                ),
                yaxis = dict(
                    title = 'Sites',
                    titlefont=dict(
                        family='Arial, sans-serif',
                        size=18,
                        color='lightgrey'
                    ),
                    showticklabels=True,
                    tickangle=45,
                    tickfont=dict(
                        family='Old Standard TT, serif',
                        size=9,
                        color='black'
                    )    
                )
            )
    }

    #fig = go.Figure(data = [trace], layout = layout)

    #plotly.offline.iplot(fig)


# In[86]:


def getBestSites_ByDate( datestr ):
    SitesByDate = riverKeeper_df[riverKeeper_df['Date'] == datestr]
    x=SitesByDate.shape[0]
 
    if x >= 1:
        SitesByDate = SitesByDate.sort_values('EnteroCount').reset_index(drop=True)  
        SitesByDate = SitesByDate.sort_values('EnteroCount',ascending=False).reset_index(drop=True)
        SitesByDate = SitesByDate[['Site','EnteroCount']]
        SafeSites = SitesByDate[SitesByDate['EnteroCount'] < 31]
    
        if SafeSites.shape[0] > 0:
            return PlotResult(SafeSites,"Safe Sites For " + datestr,"green")
        else:
            return PlotResult(SitesByDate,"Sites Are Not Safe For Swiming " + datestr,"red")
    else:
        return Graph('All Sites')
getBestSites_ByDate('2011-07-02')
print(riverKeeper_df.Date.unique())


# In[ ]:


def generate_table(dataframe, max_rows=5):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


# In[ ]:


uniqueDate=riverKeeper_df['Date'].unique()
uniqueDate= pd.Series([pd.to_datetime(d) for d in uniqueDate])

app = dash.Dash()
app.layout = html.Div(children=[
    html.H4(children='Water Quality of Swimming Sites By Date'),
    dcc.Dropdown(id='dropdown', options=[
        {'label': i, 'value': i} for i in uniqueDate
    ],placeholder='Filter by Date...'),
    html.Div(id='table-container'),
    html.Div([
    dcc.Graph(id='graph')])
])

@app.callback(
    dash.dependencies.Output('table-container','children'),
    [dash.dependencies.Input('dropdown', 'value')])

def update_rows(dropdown_value):
    if dropdown_value is None:
        return generate_table(riverKeeper_df.sort_values('EnteroCount').reset_index(drop=True))
    dff = riverKeeper_df[riverKeeper_df['Date']==dropdown_value]
    return generate_table(dff.sort_values('EnteroCount').reset_index(drop=True))

@app.callback(
    dash.dependencies.Output('graph','figure'),
    [dash.dependencies.Input('dropdown', 'value')])

def update_figure(dropdown_value):
    if dropdown_value is None:
        return Graph('All Sites')
    return getBestSites_ByDate(dropdown_value)

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
if __name__ == '__main__':
    app.run_server(debug=False,port=8028)

