from datetime import datetime
import json
import time
import mimetypes
from pathlib import Path
from uuid import uuid4

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from utils.pipeline_options import get_pipeline_options

import logging

# These will be set per-run by the main process
def init_paths(session_timestamp):
    global LOG_ROOT, OUTPUT_ROOT, summary_logger, start_global

    LOG_ROOT = Path("logs") / f"run_{session_timestamp}"
    OUTPUT_ROOT = Path("outputs") / f"run_{session_timestamp}"
    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    summary_logger = logging.getLogger("summary")
    summary_logger.setLevel(logging.INFO)
    summary_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    summary_handler = logging.FileHandler(LOG_ROOT / "summary.log")
    summary_handler.setFormatter(summary_formatter)
    summary_logger.handlers.clear()
    summary_logger.addHandler(summary_handler)

    start_global = time.time()
    return LOG_ROOT, OUTPUT_ROOT, summary_logger, start_global

def get_logger_for_file(log_dir: Path, file_stem: str):
    log_file = log_dir / f"{file_stem}.log"
    logger = logging.getLogger(file_stem)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    logger.handlers.clear()
    logger.addHandler(file_handler)

    return logger

def parse_document(file_path: str, output_dir: Path, variant: str, logger: logging.Logger):
    file_id = str(uuid4())
    file_name = Path(file_path).name

    mime_type, _ = mimetypes.guess_type(file_name)
    mime_to_format = {
        'application/pdf': InputFormat.PDF,
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': InputFormat.DOCX,
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': InputFormat.XLSX,
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': InputFormat.PPTX,
        'text/plain': InputFormat.ASCIIDOC,
        'text/html': InputFormat.HTML,
        'application/xhtml+xml': InputFormat.HTML,
        'text/csv': InputFormat.CSV,
        'image/png': InputFormat.IMAGE,
        'image/jpeg': InputFormat.IMAGE,
        'image/tiff': InputFormat.IMAGE,
        'image/bmp': InputFormat.IMAGE,
        'application/xml': InputFormat.XML_JATS,
        'application/json': InputFormat.JSON_DOCLING,
        None: InputFormat.ASCIIDOC
    }

    input_format = mime_to_format.get(mime_type)
    if not input_format:
        raise ValueError(f"Unsupported file type: {mime_type}")

    pipeline_options = get_pipeline_options(variant)

    doc_converter = DocumentConverter(
        format_options={input_format: PdfFormatOption(pipeline_options=pipeline_options)}
    )

    conv_result = doc_converter.convert(file_path)
    stem = Path(file_path).stem
    ext = Path(file_path).suffix.replace('.', '')
    base_name = f"{stem}_{ext}"

    output_subdir = output_dir / base_name
    output_subdir.mkdir(parents=True, exist_ok=True)

    (output_subdir / "data.json").write_text(
        json.dumps(conv_result.document.export_to_dict(), indent=2), encoding="utf-8"
    )
    (output_subdir / "data.txt").write_text(
        conv_result.document.export_to_text(), encoding="utf-8"
    )
    (output_subdir / "data.md").write_text(
        conv_result.document.export_to_markdown(), encoding="utf-8"
    )
    (output_subdir / "data.doctags").write_text(
        conv_result.document.export_to_doctags(), encoding="utf-8"
    )

    return base_name, output_subdir, pipeline_options
def process_file(file_path, variant="default", session_timestamp=None):
    try:
        # Don't initialize paths globally in subprocess
        log_root = Path("logs") / f"run_{session_timestamp}"
        output_root = Path("outputs") / f"run_{session_timestamp}"
        summary_log_path = log_root / "summary.log"

        stem = Path(file_path).stem
        variant_log_dir = log_root / variant
        variant_log_dir.mkdir(parents=True, exist_ok=True)
        logger = get_logger_for_file(variant_log_dir, stem)

        start_time = time.time()

        logger.info("\n==============================")
        logger.info(f"\nSTARTING: {file_path}\n")

        base_name, output_subdir, pipeline_options = parse_document(
            file_path, output_root, variant, logger
        )

        elapsed = time.time() - start_time
        logger.info(f"FINISHED: {file_path} → {output_subdir}/data.*")
        logger.info(f"Time taken: {elapsed:.2f} seconds")

        logger.info("Pipeline Options:")
        logger.info(f"- OCR: {'ENABLED' if pipeline_options.do_ocr else 'DISABLED'}")
        logger.info(f"- Table Structure: {'ENABLED' if pipeline_options.do_table_structure else 'DISABLED'}")
        logger.info(f"- Threads: {pipeline_options.accelerator_options.num_threads}")
        logger.info(f"- Device: {pipeline_options.accelerator_options.device.name}")
        logger.info("\n==============================\n")

        # Write to summary log from this subprocess
        with open(summary_log_path, "a") as summary_log:
            summary_log.write(
                f"✔ {file_path} | {elapsed:.2f}s | OCR: {'Yes' if pipeline_options.do_ocr else 'No'} | Threads: {pipeline_options.accelerator_options.num_threads} | Device: {pipeline_options.accelerator_options.device.name} | Log: {variant_log_dir / (stem + '.log')}\n"
            )

    except Exception as e:
        with open(summary_log_path, "a") as summary_log:
            summary_log.write(f"✖ {file_path} | FAILED | {e} | Log: {variant_log_dir / (stem + '.log')}\n")


def finalize_summary(session_timestamp, total_elapsed, variant=None, max_cores=None, num_files=None):
    log_root = Path("logs") / f"run_{session_timestamp}"
    output_root = Path("outputs") / f"run_{session_timestamp}"
    summary_log = log_root / "summary.log"

    logger = logging.getLogger("summary_finalize")
    handler = logging.FileHandler(summary_log, mode='a')
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    logger.info(f"\nTOTAL RUNTIME: {total_elapsed:.2f} seconds")
    if num_files is not None:
        logger.info(f"FILES PROCESSED: {num_files}")
    if variant:
        logger.info(f"VARIANT USED: {variant}")
    if max_cores:
        logger.info(f"MAX CORES USED: {max_cores}")
    logger.info(f"OUTPUTS: {output_root}")
    logger.info(f"LOGS: {log_root}\n")

