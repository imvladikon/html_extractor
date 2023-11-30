
## Task assignment 

### Description

It's in the [assignment](assignment) folder.
In short words, we need to extract the values from the html pages and put them into the JSON file.


### Design process, approach selection and experiments

It's in the [design_process](design_process) folder:

- [1_problem_definition.md](design_process/1_problem_definition.md) - Problem definition
- [2_approach_list.md](design_process/2_approach_list.md) - Approach list explanation and selection with criteria of success
- [3_experiments.md](design_process/3_experiments.md) - Experiments with the selected approaches
- [4_summary.md](design_process/4_summary.md) - Summary of the experiments and next steps

### Implementation

It's in the [data_extractor](data_extractor),
check [examples](examples) folder for the examples of the usage.

```python
from data_extractor import ExtractiveHtml2JsonTransformer

file = "10020_table.html"
html_string = open(file, "r").read()

extractor = ExtractiveHtml2JsonTransformer()
print("Extracted information:")
json_dict = extractor(html_string)
```

### Data

Put data into the [data](data) folder, so:
- `data/metadata` - metadata files
- `data/tables` - html files

### Evaluation

It's in the [evaluation](evaluation) folder.
Use `benchmark runner` to run the evaluation.

```bash
python -m evaluation.benchmark_runner --predictor {rule or extractive}
```

### Preprocessing and training

It's in the [preprocessing](preprocessing) folder.
TODO: add training script

Data exploration is also there
