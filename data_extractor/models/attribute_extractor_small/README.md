---
library_name: span-marker
tags:
- span-marker
- token-classification
- ner
- named-entity-recognition
- generated_from_span_marker_trainer
datasets:
- imvladikon/table-ner-dataset-attrs
metrics:
- precision
- recall
- f1
widget:
- text: 'Creation: 31Jul2015 Uzbekistan'
- text: 'Creation: 16Oct2013 Paraguay'
- text: Creation 28Jan2018 Seychelles
- text: Creation 20Oct2011 Ukraine
- text: Creation 2Mar2013 Djibouti
pipeline_tag: token-classification
model-index:
- name: SpanMarker
  results:
  - task:
      type: token-classification
      name: Named Entity Recognition
    dataset:
      name: Unknown
      type: imvladikon/table-ner-dataset-attrs
      split: eval
    metrics:
    - type: f1
      value: 0.9788519637462235
      name: F1
    - type: precision
      value: 0.9858012170385395
      name: Precision
    - type: recall
      value: 0.972
      name: Recall
---

# SpanMarker

This is a [SpanMarker](https://github.com/tomaarsen/SpanMarkerNER) model trained on the [imvladikon/table-ner-dataset-attrs](https://huggingface.co/datasets/imvladikon/table-ner-dataset-attrs) dataset that can be used for Named Entity Recognition.

## Model Details

### Model Description
- **Model Type:** SpanMarker
<!-- - **Encoder:** [Unknown](https://huggingface.co/unknown) -->
- **Maximum Sequence Length:** 512 tokens
- **Maximum Entity Length:** 100 words
- **Training Dataset:** [imvladikon/table-ner-dataset-attrs](https://huggingface.co/datasets/imvladikon/table-ner-dataset-attrs)
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Repository:** [SpanMarker on GitHub](https://github.com/tomaarsen/SpanMarkerNER)
- **Thesis:** [SpanMarker For Named Entity Recognition](https://raw.githubusercontent.com/tomaarsen/SpanMarkerNER/main/thesis.pdf)

### Model Labels
| Label                      | Examples                              |
|:---------------------------|:--------------------------------------|
| header.table_creation_date | "21May2021", "25Jul2008", "13Sep2022" |
| header.table_id            | "31.98", "90", "58.100.59.68.17"      |

## Uses

### Direct Use for Inference

```python
from span_marker import SpanMarkerModel

# Download from the 🤗 Hub
model = SpanMarkerModel.from_pretrained("span_marker_model_id")
# Run inference
entities = model.predict("Creation 28Jan2018 Seychelles")
```

### Downstream Use
You can finetune this model on your own dataset.

<details><summary>Click to expand</summary>

```python
from span_marker import SpanMarkerModel, Trainer

# Download from the 🤗 Hub
model = SpanMarkerModel.from_pretrained("span_marker_model_id")

# Specify a Dataset with "tokens" and "ner_tag" columns
dataset = load_dataset("conll2003") # For example CoNLL2003

# Initialize a Trainer using the pretrained model & dataset
trainer = Trainer(
    model=model,
    train_dataset=dataset["train"],
    eval_dataset=dataset["validation"],
)
trainer.train()
trainer.save_model("span_marker_model_id-finetuned")
```
</details>

<!--
### Out-of-Scope Use

*List how the model may foreseeably be misused and address what users ought not to do with the model.*
-->

<!--
## Bias, Risks and Limitations

*What are the known or foreseeable issues stemming from this model? You could also flag here known failure cases or weaknesses of the model.*
-->

<!--
### Recommendations

*What are recommendations with respect to the foreseeable issues? For example, filtering explicit content.*
-->

## Training Details

### Training Set Metrics
| Training set          | Min | Median | Max |
|:----------------------|:----|:-------|:----|
| Sentence length       | 1   | 4.4688 | 13  |
| Entities per sentence | 0   | 0.9999 | 1   |

### Training Hyperparameters
- learning_rate: 1e-05
- train_batch_size: 2
- eval_batch_size: 2
- seed: 42
- gradient_accumulation_steps: 2
- total_train_batch_size: 4
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: linear
- lr_scheduler_warmup_ratio: 0.1
- num_epochs: 4
- mixed_precision_training: Native AMP

### Training Results
| Epoch  | Step  | Validation Loss | Validation Precision | Validation Recall | Validation F1 | Validation Accuracy |
|:------:|:-----:|:---------------:|:--------------------:|:-----------------:|:-------------:|:-------------------:|
| 0.0833 | 1000  | 0.2905          | 0.0                  | 0.0               | 0.0           | 0.7683              |
| 0.1667 | 2000  | 0.0974          | 1.0                  | 0.858             | 0.9236        | 0.9613              |
| 0.25   | 3000  | 0.0487          | 0.9856               | 0.958             | 0.9716        | 0.9802              |
| 0.3333 | 4000  | 0.0306          | 0.9856               | 0.958             | 0.9716        | 0.9802              |
| 0.4167 | 5000  | 0.0236          | 0.9816               | 0.96              | 0.9707        | 0.9798              |
| 0.5    | 6000  | 0.0192          | 0.9796               | 0.962             | 0.9707        | 0.9825              |
| 0.5833 | 7000  | 0.0168          | 0.9757               | 0.962             | 0.9688        | 0.9825              |
| 0.6667 | 8000  | 0.0157          | 0.9757               | 0.964             | 0.9698        | 0.9829              |
| 0.75   | 9000  | 0.0135          | 0.9858               | 0.97              | 0.9778        | 0.9870              |
| 0.8333 | 10000 | 0.0130          | 0.9818               | 0.972             | 0.9769        | 0.9897              |
| 0.9167 | 11000 | 0.0115          | 0.9778               | 0.97              | 0.9739        | 0.9883              |
| 1.0    | 12000 | 0.0104          | 0.9838               | 0.972             | 0.9779        | 0.9910              |
| 1.0833 | 13000 | 0.0094          | 0.9818               | 0.972             | 0.9769        | 0.9892              |
| 1.1667 | 14000 | 0.0088          | 0.9858               | 0.972             | 0.9789        | 0.9906              |

### Framework Versions
- Python: 3.10.12
- SpanMarker: 1.5.0
- Transformers: 4.35.2
- PyTorch: 2.1.0+cu118
- Datasets: 2.15.0
- Tokenizers: 0.15.0

## Citation

### BibTeX
```
@software{Aarsen_SpanMarker,
    author = {Aarsen, Tom},
    license = {Apache-2.0},
    title = {{SpanMarker for Named Entity Recognition}},
    url = {https://github.com/tomaarsen/SpanMarkerNER}
}
```

<!--
## Glossary

*Clearly define terms in order to be accessible across audiences.*
-->

<!--
## Model Card Authors

*Lists the people who create the model card, providing recognition and accountability for the detailed work that goes into its construction.*
-->

<!--
## Model Card Contact

*Provides a way for people who have updates to the Model Card, suggestions, or questions, to contact the Model Card authors.*
-->