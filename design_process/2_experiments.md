

## Benchmarks results

### Results of rule-based

| Split | FP | FN | TN | TP | Precision | Recall | F1 | Accuracy | Time    | Ops/sec |
|-------| --- | --- | --- |--- |----------| --- | --- | --- |---------| --- |
| all   | 0 | 0 | 0 |  1076947 |  1.0 | 1.0 | 1.0 | 1.0 | 0:01:02 |493.86 |


Note: need to mention that rule-based was improved several times according to specific FP cases,
that were found automatically during the experiments using "catcher" class. It was about rule-based dates extraction.
And, it seems that better to replace date-extraction with NER model. 


### Results of Extractive models ("NER"-like models)

base checkpoint: [`bert-tiny`](https://huggingface.co/google/bert_uncased_L-2_H-128_A-2) (2 layers, 128 hidden, 2 heads, ~4.43M parameters)

| Split | FP | FN | TN | TP| Precision | Recall | F1 | Accuracy | Time | Ops/sec |
|-------| --- | --- | --- |--- |--------------| --- | --- | --- | --- | --- |
| all   | 6858 | 2899 | 0 |1069459 | 0.9916       | 0.9969 | 0.9941 | 0.9888 | 2:52:07 | 2.90 |

### Generative models

### Template-based approach

