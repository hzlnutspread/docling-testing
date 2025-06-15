#  Docling Testing
This repo benchmarks the performance of Docling across different configurations.

##  Installation
1. Create a virtual environment:
```
python -m venv venv
```
<br>

2. Activate the virtual environment:
```
source venv/bin/activate
```
<br>

3. Install requirements:
```
pip install -r requirements.txt
```
<br>


##  Running the Pipeline
Setup required folders:
```
mkdir input_docs logs outputs
```
<br>


Add test documents to the input folder:
- These are simple test files. Replace them with more complex documents for realistic results.
```
cp test_documents/* input_docs/
```
<br>


Run the pipeline:
```
python src/main.py --input_dir input_docs --variant ocr_t6 --max_cores 4
```
- Use --variant to set number of threads (ocr_t1 to ocr_t6)

- Use --max_cores to set number of parallel processes
<br>
<br>


##  Outputs & Logging
Processed outputs go to: outputs/run_<timestamp>/[file_name]/
- Includes .doctags, .json, .md, .txt

Logs are saved to: logs/run_<timestamp>/
- Includes per-file logs and summary.log

##  Benchmarking Results

###  Threads vs Cores (100 files )
ocr_t1 (1 thread)

✅ 1 core → 390.79s

✅ 2 cores → 195.68s

✅ 3 cores → 147.46s

✅ 4 cores → 107.22s

✅ 5 cores →  89.27s

✅ 6 cores →  82.25s

✅ 7 cores →  82.10s

✅ 8 cores →  82.92s
<br>
<br>

ocr_t2 (2 threads)

✅ 1 core → 361.69s

✅ 2 cores → 190.10s

✅ 3 cores → 132.23s

✅ 4 cores → 103.86s

✅ 5 cores →  87.48s

✅ 6 cores →  81.88s
<br>
<br>

ocr_t3 to t5 (6 cores)

✅ ocr_t3 → 76.44s

✅ ocr_t4 → 79.50s

✅ ocr_t5 → 85.13s
<br>
<br>

### File Count Scaling (6 cores, 4 threads - ocr_t4)
| Number of Files | Total Time (s) | Time per File (s) |
| --------------- | -------------- | ----------------- |
| 4               | 8.39           | 2.10              |
| 8               | 11.63          | 1.45              |
| 12              | 12.80          | 1.07              |
| 16              | 15.94          | 1.00              |
| 20              | 19.49          | 0.97              |
| 24              | 20.69          | 0.86              |
| 32              | 26.63          | 0.83              |
| 36              | 29.51          | 0.82              |
| 40              | 32.26          | 0.81              |
| 100             | 79.50          | 0.80              |
| 200             | 165.68         | 0.83              |


-  Time per file drops logarithmically and stabilizes around 0.8s/file beyond ~30–40 files.
<br>
<br>

## Conclusion
- Use as many cores as possible — scaling is strong up to 6–8.

- 4 threads per process is optimal for Docling.

- Thread count beyond 4 has diminishing returns.

- Current benchmarking used simple, one-page files — expect more variance on complex data.

--- 

<br>
 Tested on MacBook M4 Pro (6 performance cores)
