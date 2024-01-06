# -*- coding: utf-8 -*-
"""Handling of PlanktoScope data archives in the ToTS project"""

import tarfile
import tempfile
import zipfile

# Results archives

def extract_ecotaxa_export(results_archive, output_file, verbose=False):
    """Extract the EcoTaxa export archive of a results archive file to the specified output file."""
    with tarfile.open(fileobj=results_archive, mode='r:gz') as results_tar:
        export_filename = _identify_ecotaxa_export_file(results_tar)
        if verbose:
            print(f'Extracting {export_filename} from {results_archive.name}...')
        with results_tar.extractfile(export_filename) as ecotaxa_archive:
            output_file.write(ecotaxa_archive.read())
            output_file.flush()

def _identify_ecotaxa_export_file(results_tar):
    """Determine the path (within the results archive tarfile) of the EcoTaxa export archive.

    This function assumes that the results archive only has a single EcoTaxa export archive, and
    raises a ValueError if this assumption is violated.
    """
    export_file = None
    for tarinfo in results_tar:
        if not tarinfo.isreg():
            continue
        if not tarinfo.name.startswith('export/'):
            continue
        if not tarinfo.name.endswith('.zip'):
            continue
        if export_file is not None:
            raise ValueError(
                'Results archive has multiple EcoTaxa export archives, but only one is allowed',
            )
        export_file = tarinfo.name
    if export_file is None:
        raise ValueError('Couldn\'t find any EcoTaxa export archives in the results archive')
    return export_file

# EcoTaxa export archives

def update_metadata_file(input_archive, output_archive, updater, verbose=False):
    """Update the metadata file of an input EcoTaxa export archive with an updater function.

    The result is written to the output archive.

    The updater function must take one positional argument specifying a file object to the metadata
    file."""
    with tempfile.TemporaryFile(
        mode='w+', prefix='tots-ps-ecotaxa-metadata', suffix='.tsv',
    ) as ecotaxa_metadata_file:
        _extract_metadata_file(input_archive, ecotaxa_metadata_file)
        ecotaxa_metadata_file.seek(0)
        updater(ecotaxa_metadata_file)
        ecotaxa_metadata_file.seek(0)
        _replace_metadata_file(input_archive, output_archive, ecotaxa_metadata_file)

def _extract_metadata_file(ecotaxa_archive, output_file):
    """Extract the metadata file of an EcoTaxa export archive to the specified output file.

    The cursor of the output file is left at the end of the file."""
    with (
        zipfile.ZipFile(ecotaxa_archive, mode='r') as ecotaxa_zip,
        ecotaxa_zip.open('ecotaxa_export.tsv') as metadata_file,
    ):
        output_file.write(metadata_file.read().decode('utf-8'))
        output_file.flush()

def _replace_metadata_file(input_ecotaxa_export, output_ecotaxa_export, replacement_file):
    """Replace the metadata file of an input EcoTaxa export zip file with the specified file.

    The result is written to the output export file.

    The cursor of the replacement file must be at the appropriate location before the function is
    called, and it is left at the end of the file when the function returns.
    """
    with (
        zipfile.ZipFile(input_ecotaxa_export, mode='r') as input_zip,
        zipfile.ZipFile(output_ecotaxa_export, mode='w') as output_zip,
    ):
        # TODO: add all non-metadata files, and then add the metadata file
        for zipinfo in input_zip.infolist():
            if zipinfo.filename == 'ecotaxa_export.tsv':
                continue
            output_zip.writestr(zipinfo, input_zip.read(zipinfo))
        # TODO: add the metadata file
        output_zip.writestr('ecotaxa_export.tsv', replacement_file.read())
