# Preprocess the .dat file to handle irregular columns
with open('al_epsilon_sep.dat', 'r') as infile, open('cleaned_data.dat', 'w') as outfile:
    for line in infile:
        # Normalize spacing and write to a new file
        cleaned_line = ' '.join(line.split())
        outfile.write(cleaned_line + '\n')
import pandas as pd
import plotly.graph_objects as go

# Load data from the cleaned .dat file
df = pd.read_csv('cleaned_data.dat', sep='\s+', header=None,
                 names=['energy', 'interband_real', 'interband_imaginary',
                        'intraband_real', 'intraband_imaginary',
                        'total_real', 'total_imaginary'])

# Create the plot
fig = go.Figure()

# Add traces for each dataset
fig.add_trace(go.Scatter(
    x=df['energy'],
    y=df['interband_real'],
    mode='lines',
    name='Interband Real'
))

fig.add_trace(go.Scatter(
    x=df['energy'],
    y=df['interband_imaginary'],
    mode='lines',
    name='Interband Imaginary'
))

fig.add_trace(go.Scatter(
    x=df['energy'],
    y=df['intraband_real'],
    mode='lines',
    name='Intraband Real'
))

fig.add_trace(go.Scatter(
    x=df['energy'],
    y=df['intraband_imaginary'],
    mode='lines',
    name='Intraband Imaginary'
))

fig.add_trace(go.Scatter(
    x=df['energy'],
    y=df['total_real'],
    mode='lines',
    name='Total Real'
))

fig.add_trace(go.Scatter(
    x=df['energy'],
    y=df['total_imaginary'],
    mode='lines',
    name='Total Imaginary'
))

# Update layout for better visualization
fig.update_layout(
    title='Dielectric Function Plot',
    xaxis_title='Energy',
    yaxis_title='Dielectric',
    legend_title='Legend',
    template='plotly_dark'  # Optional: Set a theme
)

# Show the plot
fig.show()
fig.write_html('interactive_plot.html')
