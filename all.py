from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, show
from bokeh.models import Title
from bokeh.models import HoverTool
from bokeh.palettes import RdYlGn, Accent, Category10
from bokeh.layouts import column, row
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.transform import factor_cmap, cumsum
from math import pi
import pandas as pd
from mysql import connector


def connect_mysql():
    mydb = connector.connect(
        host="localhost",
        user="root",
        password="",
        database="uni"
    )
    return mydb

def get_students_grades():
    arr_grades = []
    mydb = connect_mysql()
    mycursor = mydb.cursor()

    # TODO Refactor code below
    #Get numer of students with grade 2.
    mycursor.execute("select * From ClassStudent where finalgrade=2;")
    grade2_results = len(mycursor.fetchall())
    arr_grades.append(grade2_results)

    #Get numer of students with grade 3.
    mycursor.execute("select * From ClassStudent where finalgrade=3;")
    grade3_results = len(mycursor.fetchall())
    arr_grades.append(grade3_results)

    # #Get numer of students with grade 4.
    mycursor.execute("select * From ClassStudent where finalgrade=4;")
    grade4_results = len(mycursor.fetchall())
    arr_grades.append(grade4_results)

    # #Get numer of students with grade 5.
    mycursor.execute("select * From ClassStudent where finalgrade=5;")
    grade5_results = len(mycursor.fetchall())
    arr_grades.append(grade5_results)

    # #Get numer of students with grade 6.
    mycursor.execute("select * From ClassStudent where finalgrade=6;")
    grade6_results = len(mycursor.fetchall())
    arr_grades.append(grade6_results)

    return arr_grades

def get_students_by_gender_and_yearStart(gender, year_start):
    
    mydb = connect_mysql()
    mycursor = mydb.cursor()
    mycursor.execute(
        "SELECT FirstName, LastName, YearStart, YearEnd, Gender FROM PERSON Left Join Student on StudentID=PersonID where YearStart={year} and Gender='{gender}';"
        .format(year=year_start, gender=gender)
    )
    query_results = mycursor.fetchall()
    count = len(query_results)

    return count

def return_data_about_students(gender):
    arr = []
    for year in years:
        students = get_students_by_gender_and_yearStart(gender, year)
        arr.append(students)

    return arr

def get_students_start_and_end_year():
    
    mydb = connect_mysql()
    mycursor = mydb.cursor()
    mycursor.execute(
        "SELECT YearStart, YearEnd FROM PERSON Left Join Student on StudentID=PersonID where YearStart != 'Null';"
    )
    query_results = mycursor.fetchall()
    two_years = 0
    three_years = 0
    four_years = 0
    more_than_four = 0
    for pair in query_results:
        year_start = pair[0]
        year_end = pair[1]
        if year_end == None:
            more_than_four = more_than_four + 1
        else :
            diff = year_end - year_start

            if diff == 1 or diff == 2:
                two_years = two_years + 1
            
            if diff == 3:
                three_years = three_years + 1
            
            if diff == 4: 
                four_years = four_years + 1
            
            if diff > 4:
                more_than_four = more_than_four + 1
    
    dictt = {
        '1-2 years': two_years,
        '3 years': three_years, 
        '4 years': four_years, 
        'more than 4 years': more_than_four, 
    }
        
    return dictt

# config
output_file("all_charts.html")
curdoc().theme = 'dark_minimal'


# First Chart
x = [2, 3, 4, 5, 6]
y = get_students_grades()

# instantiating the figure object
grades_graph = figure(title = "Number of students by Final grades", toolbar_location=None, tools=[HoverTool()],
    tooltips=" @top students with Final Grade @x.",margin=(0,0,10,0))

grades_graph.add_layout(Title(text="Students Count", align="center"), "left")
grades_graph.add_layout(Title(text="Final Grades", align="center"), "below")
    
color = RdYlGn[5][::-1]
# plotting the graph
grades_graph.vbar(x,
    top = y,
    width = 0.5,
    color= color
)
grades_graph.y_range.start = 0
grades_graph.axis.minor_tick_line_color = None


# Second Chart
years = ['2004', '2005', '2006', '2007', '2008', '2009', '2010']
genders = ['Male', 'Female']
data = {
    'year' : years,
    'Male'   : return_data_about_students('M'),
    'Female'   : return_data_about_students('F')
}
palette = Accent[6][4:6]
x = [ (year, gender) for year in years for gender in genders ]
counts = sum(zip(data['Male'], data['Female']), ()) # like an hstack
source = ColumnDataSource(data=dict(x=x, counts=counts))

gender_graph = figure(
    x_range=FactorRange(*x),
    height=250,
    title="Students started university by gender through years",
    toolbar_location=None,
    tooltips=" @counts students, @x.",
    margin=(0,0,10,0)
)

gender_graph.vbar(
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

gender_graph.y_range.start = 0
gender_graph.x_range.range_padding = 0.1
gender_graph.xaxis.major_label_orientation = 1
gender_graph.xgrid.grid_line_color = None


# Third Chart
x = get_students_start_and_end_year()
pie_data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'country'})
pie_data['angle'] = pie_data['value']/pie_data['value'].sum() * 2*pi
pie_data['color'] = Category10[len(x)]

spent_years_graph = figure(
    height=350,
    title="Years spent at university by students. Total students: 1002",
    toolbar_location=None,
    tools="hover",
    tooltips="@country: @value students",
    x_range=(-0.5, 1.0)
)

spent_years_graph.wedge(
    x=0,
    y=1, 
    radius=0.4,
    start_angle=cumsum(
        'angle',
        include_zero=True
    ), 
    end_angle=cumsum(
        'angle'
    ),
    line_color="white",
    fill_color='color',
    legend_field='country',
    source=pie_data
)

spent_years_graph.axis.axis_label = None
spent_years_graph.axis.visible = False
spent_years_graph.grid.grid_line_color = None

# displaying the charts in column view
show(column(grades_graph, gender_graph, spent_years_graph))