# importing the modules
from bokeh.io import curdoc
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.palettes import Accent


import mysql.connector

def get_students_by_gender(gender):
    
    arr_grades = []
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rakiq*Salata1",
    database="university"
    )
    mycursor = mydb.cursor()

    #Get numer of students with grade 2.
    mycursor.execute("select * From ClassStudent where finalgrade=2;")
    grade2_results = len(mycursor.fetchall())
    arr_grades.append(grade2_results)


output_file("students_yearStart_gender_graph.html")
curdoc().theme = 'dark_minimal'

#TODO Make Queries and pass data to the plot

#Data
fruits = ['2004', '2005', '2006', '2007', '2008', '2009', '2010']
years = ['Male', 'Female']


data = {'fruits' : fruits,
    'Male'   : [2, 1, 4, 3, 2, 4, 5],
    'Female'   : [5, 3, 3, 2, 4, 6, 6]
}

# this creates [ ("Apples", "2015"), ("Apples", "2016"), ("Apples", "2017"), ("Pears", "2015), ... ]
x = [ (fruit, year) for fruit in fruits for year in years ]
counts = sum(zip(data['Male'], data['Female']), ()) # like an hstack

source = ColumnDataSource(data=dict(x=x, counts=counts))

graph = figure(
    x_range=FactorRange(*x),
    height=250,
    title="Students started university by year and gender",
    toolbar_location=None, tools=""
)

palette = Accent[6][4:6]

graph.vbar(
    x='x',
    top='counts',
    width=0.9,
    source=source,
    fill_color=factor_cmap(
        'x',
        palette=palette,
        factors=years,
        start=1,
        end=2
    )
)

graph.y_range.start = 0
graph.x_range.range_padding = 0.1
graph.xaxis.major_label_orientation = 1
graph.xgrid.grid_line_color = None

# displaying the model
# show(graph)
show(graph)