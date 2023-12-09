# -*- coding: utf-8 -*-
"""Handling of PlanktoScope data archives in the ToTS project"""

import tarfile
import zipfile

# Results archives

def _untar_ecotaxa_export(results_archive, output_file, verbose=False):
    """Extract the EcoTaxa export archive of a results archive file to the specified output file."""
    with tarfile.open(fileobj=results_archive, mode='r:gz') as results_tar:
        export_filename = _identify_ecotaxa_export_file(results_tar)
        if verbose:
            print(f'Extracting {export_filename} from results archive...')
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
    return export_file

# EcoTaxa archives

def _unzip_metadata_table(ecotaxa_archive, output_file, verbose=False):
    """Extract the metadata table of an EcoTaxa export archive to the specified output file."""
    with zipfile.ZipFile(ecotaxa_archive) as ecotaxa_zip:
        with ecotaxa_zip.open('ecotaxa_export.tsv') as metadata_table:
            if verbose:
                print(f'Extracting ecotaxa_export.tsv from EcoTaxa export archive...')
            output_file.write(metadata_table.read())
            output_file.flush()
