#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Command line utility for editing metadata in EcoTaxa export archives"""

import argparse
import math
import os
import tempfile

from . import archives

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
    with tempfile.TemporaryFile(
        mode='w+b', prefix='tots-ps-ecotaxa-metadata', suffix='.tsv',
    ) as ecotaxa_metadata_table:
        with tempfile.TemporaryFile(prefix='tots-ps-', suffix='.zip') as ecotaxa_archive:
            archives._untar_ecotaxa_export(args.input, ecotaxa_archive, verbose=args.verbose)
            if args.verbose:
                print(f'Extracted EcoTaxa archive size: {_print_size(ecotaxa_archive.tell())}')
            archives._unzip_metadata_table(
                ecotaxa_archive, ecotaxa_metadata_table, verbose=args.verbose,
            )
        if args.verbose:
            print(f'Extracted metadata table size: {_print_size(ecotaxa_metadata_table.tell())}')
        #print(ecotaxa_metadata_table.seek(0))
        #print(ecotaxa_metadata_table.read())

def _print_size(size_bytes):
    """Nicely prints the size of a file.

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
