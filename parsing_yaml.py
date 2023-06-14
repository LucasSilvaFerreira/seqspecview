import yaml
import pandas as pd

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

# Your YAML file path here
yaml_file_path = "10x-RNA-v3_spec.yaml"

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

df = pd.DataFrame(data_list)

df['normalized_max_len']=[int(x) for x in 100 * (df['Max_Len']/ df['Max_Len'].sum())]
print (df['normalized_max_len'].sum())
print(df)

