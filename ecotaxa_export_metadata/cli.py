#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Command line utility for editing metadata in EcoTaxa export archives"""

import argparse
import math
import os
import tempfile

from . import ecotaxa
from . import results

def main():
    """Edit the metadata in the specified EcoTaxa export archive."""
    parser = argparse.ArgumentParser(
        prog='ecotaxa-metadata-edit',
        description='Edit the metadata of a PlanktoScope EcoTaxa dataset export archive',
    )
    parser.add_argument(
        'input',
        type=argparse.FileType(mode='rb'),
        help='Path of the results archive containing an EcoTaxa export archive to fix',
    )
    parser.add_argument(
        'output',
        type=argparse.FileType(mode='wb'),
        help='Path of the EcoTaxa export archive (with corrected metadata) to create',
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        default=False,
        help='Print additional information for troubleshooting',
    )
    args = parser.parse_args()
    # TODO: somehow get overrides as input
    overrides = {
        'process_source': 'https://github.com/PlanktoScope/PlanktoScope'
    }
    process_results_archive(args.input, args.output, overrides, verbose=args.verbose)

def process_results_archive(results_archive_file, ecotaxa_export_file, overrides, verbose=False):
    """Extract the EcoTaxa export archive from the results archive, rewriting metadata.

    The overrides dict specifies the values of metadata fields to rewrite in the EcoTaxa export
    archive.
    """
    with tempfile.TemporaryFile(prefix='tots-ps-', suffix='.zip') as ecotaxa_archive:
        results.extract_ecotaxa_export(results_archive_file, ecotaxa_archive, verbose=verbose)
        if verbose:
            print(f'Extracted EcoTaxa export archive size: {_print_size(ecotaxa_archive.tell())}')
        ecotaxa.update_metadata_file(
            ecotaxa_archive,
            ecotaxa_export_file,
            lambda metadata_file: ecotaxa.rewrite_metadata(
                metadata_file, overrides, verbose=verbose,
            ),
            verbose=verbose,
        )
        if verbose:
            print(f'Wrote updated EcoTaxa export archive to {ecotaxa_export_file.name}')

def _print_size(size_bytes):
    """Nicely print the size of a file.

    Adapted from: https://stackoverflow.com/a/14822210
    """
    if size_bytes == 0:
        return '0B'
    size_name = ('B', 'kiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB')
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    return f'{size_bytes/p:,.1f} {size_name[i]}'

if __name__ == '__main__':
    main()
