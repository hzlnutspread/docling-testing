# utils/pipeline_options.py
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.accelerator_options import AcceleratorOptions, AcceleratorDevice

def make_variant(name: str, ocr: bool, threads: int):
    opts = PdfPipelineOptions()
    opts.do_ocr = ocr
    opts.ocr_options.lang = ["en"]
    opts.do_table_structure = ocr
    if ocr:
        opts.table_structure_options.do_cell_matching = True
    opts.accelerator_options = AcceleratorOptions(
        num_threads=threads,
        device=AcceleratorDevice.AUTO
    )
    return name, opts

PIPELINE_VARIANTS = dict([
    make_variant("ocr_t1", True, 1),
    make_variant("ocr_t2", True, 2),
    make_variant("ocr_t3", True, 3),
    make_variant("ocr_t4", True, 4),
    make_variant("ocr_t5", True, 5),
    make_variant("ocr_t6", True, 6),
    make_variant("no_ocr_t1", False, 1),
    make_variant("no_ocr_t2", False, 2),
    make_variant("no_ocr_t3", False, 3),
    make_variant("no_ocr_t4", False, 4),
    make_variant("no_ocr_t5", False, 5),
    make_variant("no_ocr_t6", False, 6),
    make_variant("default", True, 4),
    make_variant("fast_no_ocr", False, 2),
    make_variant("aggressive_parallel", True, 8)
])

def get_pipeline_options(variant: str) -> PdfPipelineOptions:
    return PIPELINE_VARIANTS.get(variant, PIPELINE_VARIANTS["default"])
