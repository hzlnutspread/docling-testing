import concurrent.futures
from pathlib import Path
import argparse
import time
from datetime import datetime
import os

from utils.pipeline_options import PIPELINE_VARIANTS
from utils.processor import process_file, finalize_summary, init_paths

def main():
    parser = argparse.ArgumentParser(description="Batch document processing")
    parser.add_argument("--input_dir", type=str, default="inputs", help="Directory with files to ingest")
    parser.add_argument("--variant", type=str, default="default", choices=PIPELINE_VARIANTS.keys(), help="Pipeline variant")
    parser.add_argument("--max_cores", type=int, default=os.cpu_count(), help="Max number of cores to use for parallel processing")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    files = [str(f) for f in input_dir.iterdir() if f.is_file()]

    print(f"Found {len(files)} file(s) in '{args.input_dir}'")
    if not files:
        print("⚠️ No files found. Exiting.")
        return

    print(f"Selected pipeline variant: {args.variant}")
    print(f"Using up to {args.max_cores} core(s)")

    session_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"Session timestamp: {session_timestamp}")
    init_paths(session_timestamp)

    start_time = time.time()

    print("Submitting files to executor...")
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.max_cores) as executor:
        futures = [
            executor.submit(process_file, file_path, args.variant, session_timestamp)
            for file_path in files
        ]
        print(f"Submitted {len(futures)} job(s). Waiting for completion...")
        concurrent.futures.wait(futures)

    total_time = time.time() - start_time
    print("All jobs completed.")
    finalize_summary(session_timestamp, total_time)

    print(f"\n✅ Processed {len(files)} file(s) using '{args.variant}' in {total_time:.2f} seconds with {args.max_cores} core(s).\n")

if __name__ == "__main__":
    main()
