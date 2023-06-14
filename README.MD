## SeqSpecView
Generate a view for the seqspec.yaml file  (https://github.com/IGVF/seqspec)
---
<image src='seqspecview.png'>
This will not work with files contaning more than one hierarchy level.
This will present a separated view for each modality (considering each modality a region) See 10xCRISPR_spec.yaml.

---
This will not work with files containing more than one hierarchy level.
This will present a separate view for each modality (considering each modality a region) See 10xCRISPR_spec.yaml.


## Usage
```
python seqspecview.py seqspec.yaml
```


## Example
```
python seqspecview.py 10xCRISPR_spec.yaml
```
Open render.html to see all the views  

install

```python
pip jinja2
pip yaml
pip pandas
```


TODO
- [ ] improve the parser (parse the multi-dogmaseq spec)
- [ ] Remove duplicated regions
- [ ] show the hierarchy nodes