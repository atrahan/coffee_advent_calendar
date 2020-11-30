# myapp.py

from datetime import date
from bokeh.models.annotations import Label
from bokeh.models.widgets.markups import Div
import pandas as pd

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, TableColumn, DataTable
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc
from bokeh.io import export_png

# Files
fname_data = 'CoffeeAdventCalendarList2020.csv'

# Colors
bg_fill = "#cccccc"
bar_fill = "#2ca25f"

# Calculate daily values
if date.today().month == 12:
    day_num = min(date.today().day,25)
else:
    day_num = 1

page_title = Div(text='<h1>The Coffee Advent Calendar</h1>')

# Create the bar
bar_title = Div(text='<h2>Today</h2>')
p = figure(plot_height = 75, x_range=(0, 25), y_range=(-0.5, 0.5), toolbar_location=None)
p.border_fill_color = None
p.background_fill_color = None
p.outline_line_color = None
p.grid.grid_line_color = None

data = {'y' : [0],
       'a'   : [day_num],
       'b'   : [25 - day_num],
       }

p.hbar_stack(
    stackers=['a','b'],
    y='y',
    height=1, 
    color=[bar_fill, bg_fill], 
    source=ColumnDataSource(data)
)
# p.Label(x = day_num/2, y=0, text=f'{day_num}!', text_color='red', text_align='center', text_font_size='16pt')
lab = Label(
    x = day_num/2,
    y=0,
    text=f'{day_num}!',
    text_align='center',
    text_baseline='middle',
    text_color='red',
    text_font_size='16pt',
    text_font_style='bold',
)
p.add_layout(lab)
p.yaxis.visible = False

# Create the table
data_table_title = Div(text='<h2>Previous Days</h2>')
df_list = pd.read_csv(fname_data)
df_list = df_list[df_list['Day']<=day_num].sort_values(by='Day',ascending=False)
cds_list = ColumnDataSource(df_list)
columns = [TableColumn(field=Ci, title=Ci) for Ci in df_list.columns] # bokeh columns
data_table = DataTable(columns=columns, source=ColumnDataSource(df_list)) # bokeh table

# Today's info
today_list = df_list[df_list['Day']==day_num]
today_info = Div(text='<p style="font-size:20px">'+'</br>'.join((
        f"{'<b>Date:</b>':<22s}December {day_num}",
        f"{'<b>Brand:</b>':<22s}{today_list['Brand'].values[0]}",
        f"{'<b>Description:</b>':<22s}{today_list['Description'].values[0]}",
        f"{'<b>Roast:</b>':<22s}{today_list['Roast'].values[0]}",
    ))+"</p>"
)

# Document Layout
curdoc().add_root(column(page_title, bar_title, p, today_info, data_table_title, data_table))
