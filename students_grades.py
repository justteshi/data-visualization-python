# importing the modules
from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, show
from bokeh.models import Title
from bokeh.models import HoverTool
from bokeh.palettes import RdYlGn
from bokeh.layouts import column, row
import mysql.connector

def get_students_grades():
    arr_grades = []
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="uni"
    )
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


# file to save the model
output_file("students_grades_graph.html")
curdoc().theme = 'dark_minimal'
x = [2, 3, 4, 5, 6]
y = get_students_grades()

# instantiating the figure object
graph = figure(title = "Number of Students by Grades", toolbar_location=None, tools=[HoverTool()],
    tooltips=" @top students with Final Grade @x.",margin=(0,0,10,0))

graph.add_layout(Title(text="Students Count", align="center"), "left")
graph.add_layout(Title(text="Final Grades", align="center"), "below")
    
color = RdYlGn[5][::-1]
# plotting the graph
graph.vbar(x,
    top = y,
    width = 0.5,
    color= color
)
graph.y_range.start = 0
graph.axis.minor_tick_line_color = None

# displaying the model
# show(graph)
show(graph)