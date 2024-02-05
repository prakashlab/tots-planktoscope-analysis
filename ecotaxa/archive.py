# -*- coding: utf-8 -*-
"""Handling of PlanktoScope ecotaxa export archives"""

import zipfile

def extract_metadata_file(export_archive, output_metadata_file):
    """Extract the metadata file of an EcoTaxa export archive to the specified output file.

    The cursor of the output file is left at the end of the file."""
    with (
        zipfile.ZipFile(export_archive, mode='r') as export_zip,
        export_zip.open('ecotaxa_export.tsv') as metadata_file,
    ):
        output_metadata_file.write(metadata_file.read().decode('utf-8'))
        output_metadata_file.flush()
