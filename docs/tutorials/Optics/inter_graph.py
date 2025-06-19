with open('al_epsilon_sep.dat', 'r') as infile, open('cleaned_data.dat', 'w') as outfile:
    for line in infile:
        cleaned_line = ' '.join(line.split())
        outfile.write(cleaned_line + '\n')
from bokeh.plotting import figure, output_file, save
from bokeh.layouts import column, row
from bokeh.models import CustomJS, TextInput
import pandas as pd


df = pd.read_csv('cleaned_data.dat', sep='\s+', header=None, names=['energy', 'interband_real', 'interband_imaginary', 'intraband_real', 'intraband_imaginary', 'total_real', 'total_imaginary'])


output_file('interactive_graph_extra.html')


fig = figure(width=800, height=400, title="Dielectric Function Plot",
           x_axis_label='Energy', y_axis_label='Dielectric',
           tools="pan,wheel_zoom,box_zoom,reset")

fig.line(df['energy'], df['interband_real'], legend_label='Interband Real', line_width=2, color='blue')
fig.line(df['energy'], df['interband_imaginary'], legend_label='Interband Imaginary', line_width=2, color='red')
fig.line(df['energy'], df['intraband_real'], legend_label='Intraband Real', line_width=2, color='green')
fig.line(df['energy'], df['intraband_imaginary'], legend_label='Intraband Imaginary', line_width=2, color='purple')
fig.line(df['energy'], df['total_real'], legend_label='Total Real', line_width=2, color='orange')
fig.line(df['energy'], df['total_imaginary'], legend_label='Total Imaginary', line_width=2, color='pink')

x_min_input = TextInput(value=str(df['energy'].min()), title="x min")
x_max_input = TextInput(value=str(df['energy'].max()), title="x max")
y_min_input = TextInput(value=str(df[['interband_real', 'interband_imaginary', 'intraband_real', 'intraband_imaginary', 'total_real', 'total_imaginary']].min().min()), title="y min")
y_max_input = TextInput(value=str(df[['interband_real', 'interband_imaginary', 'intraband_real', 'intraband_imaginary', 'total_real', 'total_imaginary']].max().max()), title="y max")

callback = CustomJS(args=dict(p=fig, x_min_input=x_min_input, x_max_input=x_max_input, y_min_input=y_min_input, y_max_input=y_max_input), code="""
    let x_min = parseFloat(x_min_input.value);
    let x_max = parseFloat(x_max_input.value);
    let y_min = parseFloat(y_min_input.value);
    let y_max = parseFloat(y_max_input.value);
    p.x_range.start = x_min;
    p.x_range.end = x_max;
    p.y_range.start = y_min;
    p.y_range.end = y_max;
    p.change.emit();
""")

x_min_input.js_on_change('value', callback)
x_max_input.js_on_change('value', callback)
y_min_input.js_on_change('value', callback)
y_max_input.js_on_change('value', callback)

controls = column(x_min_input, x_max_input, y_min_input, y_max_input)
layout = row(controls, fig)

save(layout)
