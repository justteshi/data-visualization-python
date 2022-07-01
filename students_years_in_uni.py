from mysql import connector
from math import pi

import pandas as pd

from bokeh.palettes import Category10
from bokeh.plotting import figure, show
from bokeh.transform import cumsum
from bokeh.io import curdoc


def get_students_start_and_end_year():
    
    mydb = connector.connect(
    host="localhost",
    user="root",
    password="",
    database="uni"
    )
    mycursor = mydb.cursor()

    #Get numer of students with grade 2.
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


curdoc().theme = 'dark_minimal'


x = get_students_start_and_end_year()

data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'country'})
data['angle'] = data['value']/data['value'].sum() * 2*pi
data['color'] = Category10[len(x)]

p = figure(height=350, title="Years spent at university by students. Total students: 1002", toolbar_location=None,
           tools="hover", tooltips="@country: @value students", x_range=(-0.5, 1.0))

p.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='country', source=data)

p.axis.axis_label = None
p.axis.visible = False
p.grid.grid_line_color = None

show(p)

print(get_students_start_and_end_year())