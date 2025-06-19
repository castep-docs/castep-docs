import matplotlib.pyplot as plt
import pandas as pd
import itertools
from matplotlib.animation import FuncAnimation

# read data into a Pandas DataFrame
df = pd.read_csv('out.put', delim_whitespace=True, header=None, names=['gen', 'parent_child', 'member_num', 'error', 'converged', 'enth', 'vol', 'filename'])

# Only keep members that don't have an associated error with them
df = df[df['error'] == 'F']

# Colors for parents and children
color_dict = {'parents': 'red', 'children': 'blue'}

# Create plot
fig, axs = plt.subplots(1, 1, figsize=(8, 5))
scatter_size = 5

# For axis limits
noise_value = 0.5
vol_min = df['vol'].min() - noise_value
vol_max = df['vol'].max() + noise_value
enth_min = df['enth'].min() - noise_value/10
enth_max = df['enth'].max() + noise_value/10

# Manual axis limits due to outliers
# vol_min=16
# vol_max=43

# For creating the generation animation
def animate(frame):
    
    # clear previous scatterplots
    axs.clear()
    
    # filter rows where the generation matches the frame number
    df_frame = df[df['gen'] == frame]

    # Scatter plot of parents and children for this generation
    parents = df_frame[df_frame['parent_child'] == 'parent']
    children = df_frame[df_frame['parent_child'] == 'child']
    axs.scatter(parents['vol'], parents['enth'], c=color_dict['parents'], label='parents', s=scatter_size)
    axs.scatter(children['vol'], children['enth'], c=color_dict['children'], label='children', s=scatter_size)
    axs.set_xlabel('Volume (A^3/ion)')
    axs.set_ylabel('Enthalpy (eV/ion)')
    axs.grid(True,linewidth=0.5)
    axs.legend()
    axs.set_xlim([vol_min, vol_max])
    axs.set_ylim([enth_min, enth_max])
    
    # Note current generation as the title
    fig.suptitle(f'Generation {frame}')
    # fig.savefig(f'frame_{frame}.png')
    
# create animation
#anim = FuncAnimation(fig, animate, frames=range(df['gen'].min(), df['gen'].max() + 1), interval=1000)

# save animation as mp4 video file
#anim.save('animation.mp4')


#
# Now for the plot of all members (with no error)
#

fig2, axs2 = plt.subplots(figsize=(8, 5))

# Create a standard scatter plot of all members over all generations
axs2.set_xlabel('Volume (A^3/ion)')
axs2.set_ylabel('Enthalpy (eV/ion)')
axs2.grid(True, which='both',linewidth=0.5)
fig2.suptitle('All Members Over All Generations')
fig2.subplots_adjust(wspace=0.3)

axs2.set_xlim([vol_min, vol_max])
axs2.set_ylim([enth_min, enth_max])
axs2.xaxis.set_major_locator(plt.MultipleLocator(2))
axs2.xaxis.set_minor_locator(plt.MultipleLocator(0.5))
axs2.yaxis.set_major_locator(plt.MultipleLocator(1))
axs2.yaxis.set_minor_locator(plt.MultipleLocator(0.2))

axs2.scatter(df['vol'], df['enth'], s=scatter_size)

# Find the member with the lowest enthalpy value
lowest_enth_member = df[df['enth'] == df['enth'].min()]

# Position an arrow pointing at the lowest enthalpy member
arrow_start = (lowest_enth_member['vol'].values[0], lowest_enth_member['enth'].values[0])
arrow_end = (arrow_start[0] + 2, arrow_start[1])  # Position the arrow to the right of the point
axs2.annotate('', xy=arrow_start, xytext=arrow_end, arrowprops=dict(arrowstyle='->', lw=1.5))

# Label the arrow with the seed
filename = lowest_enth_member['filename'].values[0]
axs2.text(arrow_end[0] + 0.2, arrow_end[1], filename, ha='left', va='center')

plt.savefig('all_gens.png')
plt.show()

