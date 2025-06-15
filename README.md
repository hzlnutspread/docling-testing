# docling testing

this repo aims to test capabiltiies of docling

## installing

create venv
```
python -m venv venv
```

activate venv
```
source venv/bin/Activate
```

install requirements 
```
pip install -r requirements.txt
```

## running

create the required folders
```
mkdir input_docs
mkdir logs
mkdir outputs
```

copy the test documents into the `--input_docs` folder
```
cp test_documents/* input_docs/
```

```
python src/main.py --input_dir input_docs --variant ocr_t6 --max_cores 4
```

set `--variant` to set number of threads used by docling ocr e.g for 6 threads set it to:
- `ocr_t6` 

set `--max_cores` to see changes in performance
 

## outputs and logging
outputs will be in the `/outputs` folder with each file having a folder associated with itself. Each folder will contain the default docling outputs
- .doctags
- .json
- .md
- .txt

logging will be in the `/logs` folder which each run having its own folder and an overall `summary.log` file.

## benchmarking
✅ Processed 100 file(s) using 'ocr_t1' in 390.79 seconds with 1 core(s).

✅ Processed 100 file(s) using 'ocr_t1' in 195.68 seconds with 2 core(s). 

✅ Processed 100 file(s) using 'ocr_t1' in 147.46 seconds with 3 core(s). 

✅ Processed 100 file(s) using 'ocr_t1' in 107.22 seconds with 4 core(s). 

✅ Processed 100 file(s) using 'ocr_t1' in 89.27 seconds with 5 core(s).

✅ Processed 100 file(s) using 'ocr_t1' in 82.25 seconds with 6 core(s).

✅ Processed 100 file(s) using 'ocr_t1' in 82.10 seconds with 7 core(s).

✅ Processed 100 file(s) using 'ocr_t1' in 82.92 seconds with 8 core(s).


✅ Processed 100 file(s) using 'ocr_t2' in 361.69 seconds with 1 core(s).

✅ Processed 100 file(s) using 'ocr_t2' in 190.10 seconds with 2 core(s).

✅ Processed 100 file(s) using 'ocr_t2' in 132.23 seconds with 3 core(s).

✅ Processed 100 file(s) using 'ocr_t2' in 103.86 seconds with 4 core(s).

✅ Processed 100 file(s) using 'ocr_t2' in 87.48 seconds with 5 core(s).

✅ Processed 100 file(s) using 'ocr_t2' in 81.88 seconds with 6 core(s).




