from jinja2 import Environment, FileSystemLoader

import yaml
import pandas as pd
import itertools
import sys

# Your YAML file path here
#yaml_file_path = "10x-RNA-v3_spec.yaml"
yaml_file_path = sys.argv[1]



class Assay(yaml.YAMLObject):
    yaml_tag = u'!Assay'
    
    def __init__(self, assay_spec, **kwargs):
        self.assay_spec = assay_spec

class Region(yaml.YAMLObject):
    yaml_tag = u'!Region'

    def __init__(self, name, max_len=None, regions=None, **kwargs):
        self.name = name
        self.max_len = max_len
        self.regions = regions

class Onlist(yaml.YAMLObject):
    yaml_tag = u'!Onlist'

    def __init__(self, **kwargs):
        pass



data_list = []

def print_regions(region, parent=None):
    if region.regions:
        for subregion in region.regions:
            print_regions(subregion, region)
    else:
        data_list.append({
            "Region_Name": region.name,
            "Max_Len": region.max_len if region.max_len else 'No max_len',
            "Parent": parent.name if parent else None
        })

with open(yaml_file_path, 'r') as file:
    data = yaml.load(file, Loader=yaml.FullLoader)

for item in data.assay_spec:
    print_regions(item)

df_full = pd.DataFrame(data_list)



name_parents_html = []

for k, df in df_full.groupby('Parent'):
    df['normalized_max_len']=[int(x) for x in 100 * (df['Max_Len']/ df['Max_Len'].sum())]
    block_widths = df['normalized_max_len'].values.tolist()  # specify widths as percentages
    block_info = df['Parent'].values.tolist()   # specify info for each block
    block_names = df.apply(lambda x : f'{x["Region_Name"]}:({int(x["Max_Len"])})' , axis=1).values.tolist()  # specify names for each block
    #block_colors = ['#EC7063', '#58D68D', '#5499C7', '#AF7AC5'] + ['#EC7063', '#58D68D', '#5499C7', '#AF7AC5']  # specify colors for each block
    # Define color palette
    color_palette = ['#EC7063', '#58D68D', '#5499C7', '#AF7AC5', '#5D6D7E', '#48C9B0', '#F4D03F', '#EB984E']
    # Create a color iterator
    color_iter = itertools.cycle(color_palette)
    block_colors = [next(color_iter) for _ in block_widths]  # generate color for each block



    block_data = list(zip(block_widths, block_info, block_names, block_colors))

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.html')

    output = template.render(block_data=block_data, assay_name=k + ' ' + yaml_file_path)
    name = f'{k}_output.html'

    with open(name, 'w') as f:
        f.write(output)
        name_parents_html.append(name)


template = env.get_template('stack_template.html')
output = template.render(html_input=name_parents_html)

with open(f'render.html', 'w') as f:
    f.write(output)

print ('Complete: Open the render.html file to visualize the assay')