# importing the modules
from bokeh.plotting import figure, output_file, show
from bokeh.models import Title
import mysql.connector

def get_students_grades():
    arr_grades = []
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rakiq*Salata1",
    database="university"
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

print(get_students_grades())

# file to save the model
output_file("gfg.html")
      
# instantiating the figure object
graph = figure(title = "Number of Students by Grades")
graph.add_layout(Title(text="Students Count", align="center"), "left")
graph.add_layout(Title(text="Grades", align="center"), "below")

# x-coordinates to be plotted
x = [2, 3, 4, 5, 6]
  
# x-coordinates of the top edges
top = get_students_grades()
  
# width / thickness of the bars
width = 0.5
  
# plotting the graph
graph.vbar(x,
           top = top,
           width = width)
  
# displaying the model
show(graph)