#!/bin/bash

for variant in ocr_t1 ocr_t2 ocr_t3 ocr_t4 ocr_t5 ocr_t6 no_ocr_t1 no_ocr_t2 no_ocr_t3 no_ocr_t4 no_ocr_t5 no_ocr_t6
do
  for cores in {1..8}
  do
    echo "Running variant: $variant with $cores core(s)"
    python src/main.py --input_dir "input_docs" --variant $variant --max_cores $cores
  done
done
