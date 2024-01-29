#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Command line utility for editing metadata in EcoTaxa export archives"""

import argparse
import io
import json
import math
import os
import pathlib
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
        '-v', '--verbose',
        action='store_true',
        default=False,
        help='Print additional information for troubleshooting',
    )
    subparsers = parser.add_subparsers()
    setup_single_parser(subparsers.add_parser('single'))
    setup_batch_parser(subparsers.add_parser('batch'))
    args = parser.parse_args()
    args.func(args)

# single subcommand

def setup_single_parser(parser):
    """Set up a (sub)parser for editing the metadata of a single EcoTaxa export archive."""
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
    parser.set_defaults(func=lambda args: process_single_results_archive(
        args.input, args.corrections, args.output, args.changes, verbose=args.verbose,
    ))

def process_single_results_archive(
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
            print(f'  - {field}: {", ".join(field_changes["old_values"])}')
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

# batch subcommand

def setup_batch_parser(parser):
    """Set up a (sub)parser for editing the metadata of multiple EcoTaxa export archives."""
    parser.add_argument(
        'input',
        type=str,
        help='Directory of results archives, ending in `-results.tar.gz`',
    )
    parser.add_argument(
        'corrections',
        type=str,
        help='Directory of EcoTaxa metadata corrections JSON files',
    )
    parser.add_argument(
        'output',
        type=str,
        help='Directory in which to create the EcoTaxa export archives with corrected metadata',
    )
    parser.add_argument(
        'changes',
        type=str,
        help='Directory in which to create JSON files listing the metadata changes made',
    )
    parser.set_defaults(func=lambda args: process_all_results_archives(
        args.input, args.corrections, args.output, args.changes, verbose=args.verbose,
    ))

def process_all_results_archives(
    results_dir, corrections_dir, ecotaxa_export_dir, changes_dir, verbose=False,
):
    """Extract EcoTaxa export archives from the results archives, correcting metadata.

    The results archives should be provided as the path of a directory of archives. The name of each
    archive should be `{acquisition-id}-results.tar.gz`.

    The name of each metadata corrections file in the corrections directory should be
    `{acquisition-id}.json`.

    The EcoTaxa export archives with corrected metadata will be saved to the export directory. The
    name of each archive will be `{acquisition-id}-export.zip`.

    The metadata changes made for each EcoTaxa export archive according to metadata corrections will
    be saved to the changes directory. The name of each file will be `{acquisition-id}.json`.
    """
    for corrections_path in os.listdir(corrections_dir):
        corrections_path = pathlib.Path(corrections_dir).joinpath(corrections_path)
        if not corrections_path.suffix == '.json':
            if verbose:
                print(
                    f'Skipping corrections file {corrections_path} because it\'s not a JSON file!',
                )
            continue
        acq_id = corrections_path.stem
        results_path = pathlib.Path(results_dir).joinpath(acq_id + '-results.tar.gz')
        try:
            with (
                open(corrections_path, 'r') as corrections_file,
                open(results_path, 'rb') as results_file,
            ):
                export_path = pathlib.Path(ecotaxa_export_dir).joinpath(acq_id + '-export.zip')
                changes_path = pathlib.Path(changes_dir).joinpath(acq_id + '.json')
                with (
                    open(export_path, 'wb') as export_file,
                    open(changes_path, 'w') as changes_file,
                ):
                    process_single_results_archive(
                        results_file, corrections_file, export_file, changes_file, verbose=verbose,
                    )
        except OSError as e:
            print(f'Skipped {acq_id} due to an unopenable file (e.g. missing results archive): {e}')
        print()

if __name__ == '__main__':
    main()
