import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('https://docs.google.com/spreadsheets/d/1eeC-1DJtFEh0JXHLG_1VhTJo4RfkX6DyuRvQHFzpl-E/export?format=csv')


# Clean data
df = df.sort_values(by=['value'])
perc = round(1304*0.025)
df = df.iloc[perc:1304-perc]
df = df.sort_values(by=['date'])
df['date'] = pd.to_datetime(df['date'])

def draw_line_plot():
    # Draw line plot
    #     
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(df['date'],df['value'])
    ax.set(xlabel="Date",ylabel="Page Views",title="Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    date_form = DateFormatter('%Y-%m')
    ax.xaxis.set_major_formatter(date_form)
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

draw_line_plot()

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df['month_year'] = df['date'].dt.to_period('M').astype(str)
    dfbar = df.drop('date',axis=1)
    dfbar['Month'] = pd.to_datetime(dfbar['month_year']).dt.strftime('%B')
    dfbar['year'] = pd.to_datetime(dfbar['month_year']).dt.strftime('%Y')
    dfbar.drop(columns=['month_year'],inplace=True)
    
    dfbar = dfbar.groupby(['Month','year'],sort=False).mean().reset_index()
    dfbar['value'] = dfbar['value'].astype('int')
    d = dfbar.pivot(index = 'year',columns ='Month', values = 'value')
    column_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    d1 = d.reindex(column_order, axis=1)

    # Draw bar plot
    graph = d1.plot(kind="bar", rot=0)
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')    
    fig = graph.figure
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig
draw_bar_plot()

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    df_box = df_box.drop(columns=['date','index'])
    

    # Draw box plots (using Seaborn)
    fig, axs = plt.subplots(1, 2,figsize=(24,6))
    axs[0]=sns.boxplot(x = 'year',y="value",palette="Set2",hue='year',legend=False,flierprops=dict(marker= "d",markersize=1.7,fillstyle='full'),ax=axs[0],data = df_box)
    axs[0].set(xlabel="Year",ylabel="Page Views",title = 'Year-wise Box Plot (Trend)')
    axs[0].set_ylim(0, 200000)
    axs[0].locator_params(axis='y', nbins=11)
    b = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    axs[1]=sns.boxplot(x = 'month',y="value",palette="Set2",hue='month',legend=False,flierprops=dict(marker= "d",markersize=1.7,fillstyle='full'),order = b,ax=axs[1],data = df_box)
    axs[1].set(xlabel="Month",ylabel="Page Views",title = 'Month-wise Box Plot (Seasonality)')
    axs[1].set_ylim(0, 200000)
    axs[1].locator_params(axis='y', nbins=11)
   

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

draw_box_plot()
plt.show()