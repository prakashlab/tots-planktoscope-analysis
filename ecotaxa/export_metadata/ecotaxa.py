# -*- coding: utf-8 -*-
"""Handling of PlanktoScope ecotaxa export files"""

import collections
import csv
import tempfile
import zipfile

from .. import archive
from .. import metadata

# EcoTaxa export archives

def update_metadata_file(input_export_archive, output_export_archive, updater, verbose=False):
    """Update the metadata file of an input EcoTaxa export archive with an updater function.

    The result is written to the output archive.

    The updater function must take one positional argument specifying a file object to the metadata
    file. If it returns a result, that result is passed back up."""
    with tempfile.TemporaryFile(
        mode='w+', prefix='tots-ps-ecotaxa-metadata', suffix='.tsv',
    ) as metadata_file:
        archive.extract_metadata_file(input_export_archive, metadata_file)
        metadata_file.seek(0)
        result = updater(metadata_file)
        metadata_file.seek(0)
        if verbose:
            print(f'Writing updated EcoTaxa export archive to {output_export_archive.name}...')
        _replace_metadata_file(input_export_archive, output_export_archive, metadata_file)
    return result

def _replace_metadata_file(input_export_archive, output_export_archive, replacement_file):
    """Replace the metadata file of an input EcoTaxa export zip file with the specified file.

    The result is written to the output export file.

    The cursor of the replacement file must be at the appropriate location before the function is
    called, and it is left at the end of the file when the function returns.
    """
    with (
        zipfile.ZipFile(input_export_archive, mode='r') as input_zip,
        zipfile.ZipFile(output_export_archive, mode='w') as output_zip,
    ):
        for zipinfo in input_zip.infolist():
            if zipinfo.filename == 'ecotaxa_export.tsv':
                continue
            output_zip.writestr(zipinfo, input_zip.read(zipinfo))
        output_zip.writestr('ecotaxa_export.tsv', replacement_file.read())

# EcoTaxa metadata tables

def rewrite_metadata(metadata_file, overrides, verbose=False):
    """Rewrite columns of the EcoTaxa object metadata TSV file based on the dict of overrides.

    The cursor of the table file must be at the appropriate location before the function is called,
    and it is left at the end of the file."""
    field_types, data_rows = metadata.read_file(metadata_file)
    if verbose:
        print(f'Number of objects: {len(data_rows)}')
    updated_fields = _rewrite_row_fields(data_rows, overrides)
    metadata_file.seek(0)
    metadata_file.truncate()
    metadata.write_file(metadata_file, field_types, data_rows)
    return updated_fields

def _rewrite_row_fields(data_rows, overrides):
    """Update the values of certain fields of each row based on the dict of overrides."""
    updated_columns = collections.defaultdict(set)
    for row in data_rows:
        for key, value in overrides.items():
            old_value = row[key]
            if old_value != value:
                updated_columns[key].add(old_value)
                row[key] = value
    return updated_columns
