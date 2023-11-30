
# Problem Definition

## Problem Statement

Given:
- A set of html files
- A set of metadata files (assuming that it's our labelling data, which will not be provided in the production environment)

Goal:
- To build a black-box (model or app) that transforms the html files into a set of metadata files

Criteria of success:
- TODO: formulate and check with lead data scientist and the stakeholders
- e.g. the model/app should be able to process 1000 html files in 1 hour with accuracy greater than 90%


## Example of the input and output

An example of the `29999_table`

### Input


```html
<table id="Table6291Doctorhospital">
<caption>Table 62.91 Doctor, hospital</caption>
<thead>
<tr>
<th> </th>
<th>   Kathleen Peters   </th>
<th>   Glen Jones   </th>
<th>   Alexis Decker   </th>
</tr>
</thead>
<tbody>
<tr>
<td align="left" style="font-weight:bold">   Cummings, Weaver and Mitchell   </td>
<td align="left" style="font-weight:bold; font-style:italic">   338   </td>
<td align="left">   1133   </td>
<td align="left" style="font-style:italic">   353   </td>
</tr>
<tr>
<td align="left" style="font-weight:bold">   Mckenzie Ltd   </td>
<td align="left" style="font-weight:bold; font-style:italic">   1382   </td>
<td align="left">   91%   </td>
<td align="left" style="font-style:italic">   15   </td>
</tr>
</tbody><tfoot><tr><td>Creation: 18Sep2016 Latvia</td></tr></tfoot>
</table>

```

### Output

```json
{
    "body": {
        "content": [
            "338",
            "1133",
            "353",
            "1382",
            "91%",
            "15"
        ],
        "headers": {
            "col": [
                "Cummings, Weaver and Mitchell",
                "Mckenzie Ltd"
            ],
            "row": [
                "Kathleen Peters",
                "Glen Jones",
                "Alexis Decker"
            ]
        }
    },
    "footer": {
        "table_creation_date:": "18Sep2016",
        "text": "Creation: 18Sep2016 Latvia"
    },
    "header": {
        "table_id": "62.91",
        "text": "Table 62.91 Doctor, hospital"
    }
}
```


