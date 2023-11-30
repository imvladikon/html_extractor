---
library_name: span-marker
tags:
- span-marker
- token-classification
- ner
- named-entity-recognition
- generated_from_span_marker_trainer
datasets:
- imvladikon/table-ner-dataset
metrics:
- precision
- recall
- f1
widget:
- text: '<td align="left " style="font - weight: bold "> 467% </td> [SEP] [PATH] [''
    tbody'','' tr'','' td''] [ROW_NUMBER] 2 [COLUMN_NUMBER] 2 [SEP]'
- text: '<td align="left " style="font - weight: bold "> Anderson Ltd </td> [SEP]
    [PATH] ['' tbody'','' tr'','' td''] [ROW_NUMBER] 4 [COLUMN_NUMBER] 0 [SEP]'
- text: '<td align="left " style="font - weight: bold "> 31% </td> [SEP] [PATH] [''
    tbody'','' tr'','' td''] [ROW_NUMBER] 5 [COLUMN_NUMBER] 2 [SEP]'
- text: '<td align="left " style="font - weight: bold "> 618 </td> [SEP] [PATH] [''
    tbody'','' tr'','' td''] [ROW_NUMBER] 7 [COLUMN_NUMBER] 3 [SEP]'
- text: '<td align="left " style="font - weight: bold "> 38 </td> [SEP] [PATH] [''
    tbody'','' tr'','' td''] [ROW_NUMBER] 2 [COLUMN_NUMBER] 2 [SEP]'
pipeline_tag: token-classification
model-index:
- name: SpanMarker
  results:
  - task:
      type: token-classification
      name: Named Entity Recognition
    dataset:
      name: Unknown
      type: imvladikon/table-ner-dataset
      split: eval
    metrics:
    - type: f1
      value: 1.0
      name: F1
    - type: precision
      value: 1.0
      name: Precision
    - type: recall
      value: 1.0
      name: Recall
---

# SpanMarker

This is a [SpanMarker](https://github.com/tomaarsen/SpanMarkerNER) model trained on the [imvladikon/table-ner-dataset](https://huggingface.co/datasets/imvladikon/table-ner-dataset) dataset that can be used for Named Entity Recognition.

## Model Details

### Model Description
- **Model Type:** SpanMarker
<!-- - **Encoder:** [Unknown](https://huggingface.co/unknown) -->
- **Maximum Sequence Length:** 512 tokens
- **Maximum Entity Length:** 100 words
- **Training Dataset:** [imvladikon/table-ner-dataset](https://huggingface.co/datasets/imvladikon/table-ner-dataset)
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Repository:** [SpanMarker on GitHub](https://github.com/tomaarsen/SpanMarkerNER)
- **Thesis:** [SpanMarker For Named Entity Recognition](https://raw.githubusercontent.com/tomaarsen/SpanMarkerNER/main/thesis.pdf)

### Model Labels
| Label            | Examples                                                                                                                                     |
|:-----------------|:---------------------------------------------------------------------------------------------------------------------------------------------|
| body.content     | "75", "118", "30 %"                                                                                                                          |
| body.headers.col | "Holloway - Jones", "Meza - Best", "Mcconnell Inc"                                                                                           |
| body.headers.row | "Stephen Obrien", "Michelle Smith", "Darrell Long"                                                                                           |
| footer.text      | "Creation : 29Aug2020 Norfolk Island", "Creation : 29Mar2009 Maldives", "Creation : 4Apr2013 Dominican Republic"                             |
| header.table_id  | "Table84545459Outdooractivitieseducationmanager", "Table152639725356Facilitiesmanager", "Table10111552Dancemovementpsychotherapist"          |
| header.text      | "Table 71 Patent examiner", "Table 21.77.14.45 Chartered public finance accountant", "Table 35.3.35.86.33 Special educational needs teacher" |

## Uses

### Direct Use for Inference

```python
from span_marker import SpanMarkerModel

# Download from the 🤗 Hub
model = SpanMarkerModel.from_pretrained("span_marker_model_id")
# Run inference
entities = model.predict("<td align=\"left \" style=\"font - weight: bold \"> 618 </td> [SEP] [PATH] [' tbody',' tr',' td'] [ROW_NUMBER] 7 [COLUMN_NUMBER] 3 [SEP]")
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
| Training set          | Min | Median  | Max |
|:----------------------|:----|:--------|:----|
| Sentence length       | 19  | 41.5987 | 60  |
| Entities per sentence | 0   | 0.9711  | 1   |

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
| 0.0160 | 1000  | 1.3874          | 0.0                  | 0.0               | 0.0           | 0.4605              |
| 0.0319 | 2000  | 0.4606          | 0.0                  | 0.0               | 0.0           | 0.9552              |
| 0.0479 | 3000  | 0.0979          | 0.0                  | 0.0               | 0.0           | 0.9552              |
| 0.0638 | 4000  | 0.0309          | 0.0                  | 0.0               | 0.0           | 0.9552              |
| 0.0798 | 5000  | 0.0163          | 0.0                  | 0.0               | 0.0           | 0.9552              |
| 0.0957 | 6000  | 0.0124          | 0.0                  | 0.0               | 0.0           | 0.9552              |
| 0.1117 | 7000  | 0.0100          | 0.0                  | 0.0               | 0.0           | 0.9552              |
| 0.1277 | 8000  | 0.0076          | 0.0                  | 0.0               | 0.0           | 0.9552              |
| 0.1436 | 9000  | 0.0056          | 0.0                  | 0.0               | 0.0           | 0.9552              |
| 0.1596 | 10000 | 0.0047          | 0.0                  | 0.0               | 0.0           | 0.9552              |
| 0.1755 | 11000 | 0.0040          | 0.6290               | 0.4474            | 0.5229        | 0.9698              |
| 0.1915 | 12000 | 0.0032          | 0.5523               | 0.4247            | 0.4802        | 0.9681              |
| 0.2074 | 13000 | 0.0025          | 0.8428               | 0.7072            | 0.7691        | 0.9800              |
| 0.2234 | 14000 | 0.0020          | 0.8195               | 0.7113            | 0.7616        | 0.9801              |
| 0.2394 | 15000 | 0.0014          | 0.8365               | 0.7175            | 0.7725        | 0.9805              |
| 0.2553 | 16000 | 0.0012          | 0.8578               | 0.7464            | 0.7982        | 0.9822              |
| 0.2713 | 17000 | 0.0009          | 0.8863               | 0.7876            | 0.8341        | 0.9859              |
| 0.2872 | 18000 | 0.0008          | 0.9240               | 0.8268            | 0.8727        | 0.9888              |
| 0.3032 | 19000 | 0.0006          | 0.9429               | 0.8845            | 0.9128        | 0.9916              |
| 0.3191 | 20000 | 0.0005          | 0.9440               | 0.9031            | 0.9231        | 0.9935              |
| 0.3351 | 21000 | 0.0005          | 0.9447               | 0.9155            | 0.9298        | 0.9946              |
| 0.3511 | 22000 | 0.0004          | 0.9415               | 0.9299            | 0.9357        | 0.9958              |
| 0.3670 | 23000 | 0.0003          | 0.9455               | 0.9299            | 0.9376        | 0.9959              |
| 0.3830 | 24000 | 0.0003          | 0.9454               | 0.9278            | 0.9365        | 0.9957              |
| 0.3989 | 25000 | 0.0002          | 0.9770               | 0.9629            | 0.9699        | 0.9976              |
| 0.4149 | 26000 | 0.0002          | 0.9814               | 0.9794            | 0.9804        | 0.9988              |
| 0.4309 | 27000 | 0.0001          | 0.9959               | 0.9959            | 0.9959        | 0.9997              |
| 0.4468 | 28000 | 0.0001          | 0.9979               | 0.9897            | 0.9938        | 0.9990              |
| 0.4628 | 29000 | 0.0001          | 0.9979               | 0.9959            | 0.9969        | 0.9997              |
| 0.4787 | 30000 | 0.0001          | 0.9979               | 0.9959            | 0.9969        | 0.9997              |
| 0.4947 | 31000 | 0.0001          | 1.0                  | 1.0               | 1.0           | 1.0                 |
| 0.5106 | 32000 | 0.0001          | 1.0                  | 1.0               | 1.0           | 1.0                 |
| 0.5266 | 33000 | 0.0000          | 1.0                  | 1.0               | 1.0           | 1.0                 |
| 0.5426 | 34000 | 0.0000          | 1.0                  | 1.0               | 1.0           | 1.0                 |
| 0.5585 | 35000 | 0.0000          | 1.0                  | 1.0               | 1.0           | 1.0                 |
| 0.5689 | 35654 | 0.0000          | 1.0                  | 1.0               | 1.0           | 1.0                 |

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