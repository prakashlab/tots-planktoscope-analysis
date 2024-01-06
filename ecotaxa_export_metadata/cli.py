#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Command line utility for editing metadata in EcoTaxa export archives"""

import argparse
import io
import json
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
        'corrections',
        type=argparse.FileType(mode='r'),
        help='Path of a JSON file consisting of an object with field names and corrected values',
    )
    parser.add_argument(
        'output',
        type=argparse.FileType(mode='wb'),
        help='Path of the EcoTaxa export archive (with corrected metadata) to create',
    )
    parser.add_argument(
        'changes',
        type=argparse.FileType(mode='w'),
        help='Path of JSON file to create listing the changes made',
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        default=False,
        help='Print additional information for troubleshooting',
    )
    args = parser.parse_args()
    process_results_archive(
        args.input, args.corrections, args.output, args.changes, verbose=args.verbose,
    )

def process_results_archive(
    results_archive_file, corrections, ecotaxa_export_file, changes_file, verbose=False,
):
    """Extract the EcoTaxa export archive from the results archive, correcting metadata.

    The corrections dict specifies the values of metadata fields to correct in the EcoTaxa export
    archive; it can instead be provided as a file-like object containing a JSON string representing
    the corrections dict.

    Changes made to the metadata are recorded as a JSON string in the changes file.
    """
    if isinstance(corrections, io.IOBase):
        corrections = json.load(corrections)
    if verbose:
        print('Corrections to make where needed:')
        for field, value in corrections.items():
            print(f'  - {field}: {value}')
    with tempfile.TemporaryFile(prefix='tots-ps-', suffix='.zip') as ecotaxa_archive:
        if verbose:
            print(f'Loading results archive {results_archive_file.name}...')
        results.extract_ecotaxa_export(results_archive_file, ecotaxa_archive, verbose=verbose)
        if verbose:
            print(f'Extracted EcoTaxa export archive size: {_print_size(ecotaxa_archive.tell())}')
        updated_fields = ecotaxa.update_metadata_file(
            ecotaxa_archive,
            ecotaxa_export_file,
            lambda metadata_file: ecotaxa.rewrite_metadata(
                metadata_file, corrections, verbose=verbose,
            ),
            verbose=verbose,
        )
    changes = {}
    for field, old_values in updated_fields.items():
        changes[field] = {
            'new_value': corrections[field],
            'old_values': sorted(list(old_values)),
        }
    if verbose:
        print('Changes (with previous values):')
        for field, field_changes in changes.items():
            print(f'  - {field}: {', '.join(field_changes['old_values'])}')
        print(f'Recording changes to {changes_file.name}...')
    json.dump(changes, changes_file, indent=2)

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
