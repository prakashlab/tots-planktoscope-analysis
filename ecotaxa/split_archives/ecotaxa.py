# -*- coding: utf-8 -*-
"""Handling of PlanktoScope ecotaxa export files"""

import collections
import csv
import tempfile
import zipfile

from .. import archive
from .. import metadata

# EcoTaxa export archives

def chunk_archive(input_archive, num_chunks, chunk_index, output_archive, verbose=False):
    """Copy the specified chunk of the input archive to the output archive.

    The input archive is not modified.
    """
    with tempfile.TemporaryFile(
        mode='w+', prefix='tots-ps-ecotaxa-metadata', suffix='.tsv',
    ) as metadata_file:
        archive.extract_metadata_file(input_archive, metadata_file)
        metadata_file.seek(0)
        data_rows = _chunk_metadata(
            metadata_file, num_chunks, chunk_index, metadata_file,
            verbose=verbose,
        )
        if verbose:
            print(f'Writing metadata to {output_archive.name}...')
        with (
            zipfile.ZipFile(output_archive, mode='w') as output_zip,
            zipfile.ZipFile(input_archive, mode='r') as input_zip,
        ):
            metadata_file.seek(0)
            output_zip.writestr('ecotaxa_export.tsv', metadata_file.read())
            for data_row in data_rows:
                image_path = data_row['img_file_name']
                output_zip.writestr(image_path, input_zip.read(image_path))

# EcoTaxa metadata tables

def _chunk_metadata(metadata_file, num_chunks, chunk_index, output_file, verbose=False):
    """Rewrite the EcoTaxa object metadata TSV file to only include the specified chunk.

    Returns the rows of the specified chunk.

    The cursor of the table file must be at the appropriate location before the function is called,
    and it is left at the end of the file."""
    field_types, data_rows = metadata.read_file(metadata_file)
    if verbose:
        print(f'  Number of objects in all chunks: {len(data_rows)}')
    chunks = list(_chunk_rows(data_rows, num_chunks))
    data_rows = chunks[chunk_index]
    if verbose:
        print(f'  Number of objects in chunk {chunk_index}: {len(data_rows)}')
        print(f'  Images: {data_rows[0]["img_file_name"]}, {data_rows[1]["img_file_name"]}, ...')
    output_file.seek(0)
    output_file.truncate()
    metadata.write_file(output_file, field_types, data_rows)
    return data_rows

def _chunk_rows(data_rows, num_chunks):
    """Split up the provided list of rows into the specified number of lists."""
    for i in range(0, num_chunks):
        yield data_rows[i::num_chunks]
