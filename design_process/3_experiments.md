

## Benchmarks results

### Results of rule-based

| Split | FP | FN | TN | Precision | Recall | F1 | Accuracy |
|-------| --- | --- | --- | --- | --- | --- | --- |
| all   | 0 | 0 | 210000 | 1.0 | 1.0 | 1.0 | 1.0 |


Note: need to mention that rule-based was improved several times according to specific FP cases,
that were found automatically during the experiments using "catcher" class. It was about rule-based dates extraction.
And, it seems that better to replace date-extraction with NER model. 


### Results of Extractive("NER") model
