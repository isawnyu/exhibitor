# exhibitor: prepare data for ISAW website exhibitions

Exhibitor is the work of Tom Elliott (tom.elliott@nyu.edu). Copyright (c) 2019 New York University. See LICENSE.txt file for complete license.

## How to execute the processing pipeline

1. Convert the excel file provided by the Exhibitions team from their Checklist database into CSV (UTF-8 encoded)

    - Manually open in Excel and "save as" CSV (UTF-8)

2. Convert the raw CSV file to JSON

    - ```python scripts/ishtar2json.py ../../I/ishtar/checklist_data/TEST_Ishtar_8_21_19.csv ~/scratch/ishtar.json```

3. Run preparatory fixup script

    - ```python scripts/ishtar_prep.py ~/scratch/ishtar.json ~/scratch/ishtar_result.json```

4. Convert those results to the JSON form that the website batch update/load script expects

    - ```python scripts/json4plone.py '/exhibitions/ishtar-gate/objects/' ~/scratch/ishtar_result.json ~/scratch/ishtar4plone.json```

5. Copy the resulting JSON file to the server and then run the batch update script (dry run, then for real)

    - ```bin/client1 run scripts/batch_update.py --dry-run --site isaw /home/telliott/ishtar4plone.json```
    - ```bin/client1 run scripts/batch_update.py --site isaw /home/telliott/ishtar4plone.json```    

## How to customize the processing pipeline

For each new exhibition, you will probably need three new modules:

- ```exhibitor/{exhibname}{year}.py```: customizations of classes defined in ```exhibitor/objects.py```
- ```scripts/{exhibname}2json.py```: code to execute step 2, above
- ```scripts/prep_{exhibname}.py```: code to do all the cleanups and unique stuff (step 3, above)
 
## How to run tests (using nose)

```bash
nosetests -s --nologcapture --with-coverage --cover-erase --cover-html --cover-html-dir=cover --cover-package=exhibitor
```
