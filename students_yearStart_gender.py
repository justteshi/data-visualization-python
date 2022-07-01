# importing the modules
from bokeh.io import curdoc
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.palettes import Accent
from bokeh.models import HoverTool


import mysql.connector

def get_students_by_gender_and_yearStart(gender, year_start):
    
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="uni"
    )
    mycursor = mydb.cursor()

    #Get numer of students with grade 2.
    mycursor.execute(
        "SELECT FirstName, LastName, YearStart, YearEnd, Gender FROM PERSON Left Join Student on StudentID=PersonID where YearStart={year} and Gender='{gender}';".
        format(year=year_start, gender=gender)
    )
    query_results = mycursor.fetchall()
    count = len(query_results)


    return count


years = ['2004', '2005', '2006', '2007', '2008', '2009', '2010']
genders = ['Male', 'Female']

def return_data_about_students(gender):
    arr = []

    for year in years:
        students = get_students_by_gender_and_yearStart(gender, year)
        arr.append(students)

    return arr



output_file("students_yearStart_gender_graph.html")
curdoc().theme = 'dark_minimal'

#TODO Make Queries and pass data to the plot

#Data


data = {'year' : years,
    'Male'   : return_data_about_students('M'),
    'Female'   : return_data_about_students('F')
}

# this creates [ ("Apples", "2015"), ("Apples", "2016"), ("Apples", "2017"), ("Pears", "2015), ... ]
x = [ (year, gender) for year in years for gender in genders ]
counts = sum(zip(data['Male'], data['Female']), ()) # like an hstack

source = ColumnDataSource(data=dict(x=x, counts=counts))

graph = figure(
    x_range=FactorRange(*x),
    height=250,
    title="Students started university by gender through years",
    toolbar_location=None,
    tooltips=" @counts students, @x.",
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
        factors=genders,
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