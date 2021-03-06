# coffeecalendar.py

from datetime import datetime, timedelta
from bokeh.models.annotations import Label
from bokeh.models.widgets.markups import Div
import pandas as pd

from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, TableColumn, DataTable
from bokeh.plotting import figure, curdoc

# Files
fname_data = 'coffeecalendar/CoffeeAdventCalendarList2020.csv'

# Colors
bg_fill = "#cccccc"
bar_fill = "#2ca25f"

# Calculate daily values
cur_dt = datetime.now() - timedelta(hours=8)
day_num = min(cur_dt.day, 25)
# if cur_dt.month == 12:
#     day_num = min(cur_dt.day,25)
# else:
#     day_num = 1

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
    ))+"</p>", width=470
)

logo_image = (
    today_list['Brand'].values[0]
    .replace(" ", "")
    .replace("'", "")
    + ".png"
)
today_logo = Div(
    text=" ".join(
        (
            f'<img src="coffeecalendar/static/{logo_image}"',
            f'alt="{today_list["Brand"].values[0]}"',
            'style="width:130px;height:130px;top:5px"',
            'align="middle">',
        )
    )
)

# Document Layout
dash_layout = column(
    page_title, bar_title, p, row(today_logo, today_info, width=600), data_table_title, data_table,)
curdoc().add_root(dash_layout)
