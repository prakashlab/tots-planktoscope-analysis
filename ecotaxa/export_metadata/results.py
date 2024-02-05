# -*- coding: utf-8 -*-
"""Handling of PlanktoScope results archives in the ToTS project"""

import tarfile

def extract_ecotaxa_export(results_archive, output_file, verbose=False):
    """Extract the EcoTaxa export archive of a results archive file to the specified output file."""
    with tarfile.open(fileobj=results_archive, mode='r:gz') as results_tar:
        export_filename = _identify_ecotaxa_export_file(results_tar)
        if verbose:
            print(f'Extracting {export_filename}...')
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
