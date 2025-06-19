import pandas as pd
import math
read_dict = {}
i = 0
section_results = []
line_skipped = False
with open("Al_epsilon.dat","r") as f:
  for line in f:
    if "#" in line:
      continue
    line_split = line.split(" ")
    if line_skipped == False and len(line_split) == 2:
      line_skipped = True
      continue
    if line_skipped == True and len(line_split) == 2:
       
       read_dict[i] = section_results
       i += 1
       section_results = []
       continue
    line_skipped = False 
    clean_line_split = []
    for x in line_split:
      if x.strip() and  math.isnan(float(x)):
        clean_line_split.append(0)
        continue
      if x.strip():
        clean_line_split.append(float(x))
    section_results.append(clean_line_split)

read_dict[i] = section_results
def clean(inp):
  return inp  
with open("Al_epsilon_sep.dat","w") as f:
  col1  = []    #energy  = dict[a][x][0] a gonna use 1
  col2  = []    #interband real  = dict[1][x][1]
  col3  = []    #interband imaginary = dict[1][x][2]
  col4  = []    #intraband real = dict[2][x][1]
  col5  = []    #intraband imaginary = dict[2][x][2]
  col6  = []    #total real = dict[3][x][1]
  col7  = []    #total imaginary = dict[3][x][2]
  one = read_dict[1]
  two = read_dict[2]
  thr = read_dict[3]
  for arr in one:
    col1.append(clean(arr[0]))
    col2.append(clean(arr[1]))
    col3.append(clean(arr[2]))
  for arr in two:
    col4.append(clean(arr[1]))
    col5.append(clean(arr[2]))
  for arr in thr:
    col6.append(clean(arr[1]))
    col7.append(clean(arr[2]))
  df = pd.DataFrame({
    'energy': col1,
    'interband_real': col2,
    'interband_imaginary': col3,
    'intraband_real': col4,
    'intraband_imaginary': col5,
    'total_real': col6,
    'total_imaginary': col7
  })
  for row in df.itertuples(index=False, name=None):
    formatted_line = "    ".join(f"{x:25.16f}" for x in row)
    f.write(formatted_line + "\n")
