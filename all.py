from math import pi

from bokeh.io import curdoc, output_file, show
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, FactorRange, HoverTool, Title
from bokeh.palettes import Accent, Category10, RdYlGn
from bokeh.plotting import figure
from bokeh.transform import cumsum, factor_cmap

from src.analytics import (
    get_grade_distribution,
    get_student_enrollment_by_gender_and_year,
    get_study_duration_distribution,
)


YEARS = (2004, 2005, 2006, 2007, 2008, 2009, 2010)
GENDERS = (("M", "Male"), ("F", "Female"))


output_file("all_charts.html")
curdoc().theme = "dark_minimal"


# First chart: final-grade distribution.
grade_distribution = get_grade_distribution()
grades = list(grade_distribution)
grades_graph = figure(
    title="Number of students by Final grades",
    toolbar_location=None,
    tools=[HoverTool()],
    tooltips=" @top students with Final Grade @x.",
    margin=(0, 0, 10, 0),
)
grades_graph.add_layout(Title(text="Students Count", align="center"), "left")
grades_graph.add_layout(Title(text="Final Grades", align="center"), "below")
grades_graph.vbar(
    grades,
    top=[grade_distribution[grade] for grade in grades],
    width=0.5,
    color=RdYlGn[5][::-1],
)
grades_graph.y_range.start = 0
grades_graph.axis.minor_tick_line_color = None


# Second chart: student enrollment by gender and year.
enrollment_counts = get_student_enrollment_by_gender_and_year()
gender_labels = [label for _, label in GENDERS]
gender_factors = [(str(year), label) for year in YEARS for label in gender_labels]
counts = [
    enrollment_counts.get((year, code), 0)
    for year in YEARS
    for code, _ in GENDERS
]
source = ColumnDataSource(data={"x": gender_factors, "counts": counts})

gender_graph = figure(
    x_range=FactorRange(*gender_factors),
    height=250,
    title="Students started university by gender through years",
    toolbar_location=None,
    tooltips=" @counts students, @x.",
    margin=(0, 0, 10, 0),
)
gender_graph.vbar(
    x="x",
    top="counts",
    width=0.9,
    source=source,
    fill_color=factor_cmap(
        "x", palette=Accent[6][4:6], factors=gender_labels, start=1, end=2
    ),
)
gender_graph.y_range.start = 0
gender_graph.x_range.range_padding = 0.1
gender_graph.xaxis.major_label_orientation = 1
gender_graph.xgrid.grid_line_color = None


# Third chart: study-duration distribution.
duration_distribution = get_study_duration_distribution()
duration_labels = list(duration_distribution)
duration_values = [duration_distribution[label] for label in duration_labels]
duration_source = ColumnDataSource(
    data={
        "country": duration_labels,
        "value": duration_values,
        "angle": [value / sum(duration_values) * 2 * pi for value in duration_values],
        "color": Category10[len(duration_labels)],
    }
)

spent_years_graph = figure(
    height=350,
    title=f"Years spent at university by students. Total students: {sum(duration_values)}",
    toolbar_location=None,
    tools="hover",
    tooltips="@country: @value students",
    x_range=(-0.5, 1.0),
)
spent_years_graph.wedge(
    x=0,
    y=1,
    radius=0.4,
    start_angle=cumsum("angle", include_zero=True),
    end_angle=cumsum("angle"),
    line_color="white",
    fill_color="color",
    legend_field="country",
    source=duration_source,
)
spent_years_graph.axis.axis_label = None
spent_years_graph.axis.visible = False
spent_years_graph.grid.grid_line_color = None


show(column(grades_graph, gender_graph, spent_years_graph))
