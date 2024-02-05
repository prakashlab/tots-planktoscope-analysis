#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Command line utility for splitting EcoTaxa export archives"""

import argparse
import io
import json
import math
import os
import pathlib
import tempfile

from . import ecotaxa

def main():
    """Split the specified EcoTaxa export archive(s)."""
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
    """Set up a (sub)parser for splitting a single EcoTaxa export archive."""
    parser.add_argument(
        'input',
        type=str,
        help='Path of the EcoTaxa export archive to split',
    )
    parser.add_argument(
        'num_chunks',
        type=int,
        help='Number of chunks to split the EcoTaxa export archive into',
    )
    parser.add_argument(
        'output',
        type=str,
        help='Directory in which to save the split-up EcoTaxa export archive chunks',
    )
    parser.set_defaults(func=lambda args: process_single_ecotaxa_archive(
        args.input, args.num_chunks, args.output, verbose=args.verbose,
    ))

def process_single_ecotaxa_archive(input_path, num_chunks, output_dir_path, verbose=False):
    """Split the EcoTaxa export archive into the specified number of chunks.

    The resulting chunks are saved to the specified output directory, each with a "-chunk{number}"
    suffix appended before the ".zip" file extension.
    """
    input_path = pathlib.Path(input_path)
    with open(input_path, 'rb') as input_file:
        if verbose:
            input_file.seek(0, os.SEEK_END)
            print(f'EcoTaxa export archive size: {_print_size(input_file.tell())}')
            input_file.seek(0)
        for i in range(num_chunks):
            output_dir_path = pathlib.Path(output_dir_path)
            output_path = f'{output_dir_path / input_path.stem}-chunk{i}.zip'
            if verbose:
                print(f'Writing {output_path}...')
            with open(output_path, 'wb') as output_file:
                ecotaxa.chunk_archive(input_file, num_chunks, i, output_file, verbose=verbose)
        # TODO: split up the metadata table into num_chunks sub-tables
        # TODO: copy the image from each row of each metadata table into the corresponding chunk
        # TODO: actually split the file

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
        help='Directory of EcoTaxa export archives',
    )
    parser.add_argument(
        'num_chunks',
        type=int,
        help='Number of chunks to split each EcoTaxa export archive into',
    )
    parser.add_argument(
        'output',
        type=str,
        help='Directory in which to save the split-up EcoTaxa export archive chunks',
    )
    parser.set_defaults(func=lambda args: process_all_ecotaxa_archives(
        args.input, args.num_chunks, args.output, verbose=args.verbose,
    ))

def process_all_ecotaxa_archives(input_dir, num_chunks, output_dir, verbose=False):
    """Split all EcoTaxa export archives into the specified number of chunks per archive.

    The EcoTaxa archives should be provided as the path of a directory of archives.

    The split EcoTaxa export archive chunks will be saved to the export directory, each with a
    "-chunk{number}" suffix appended before the ".zip" file extension.
    """
    for archive_path in os.listdir(input_dir):
        archive_path = pathlib.Path(input_dir).joinpath(archive_path)
        if not archive_path.suffix == '.zip':
            if verbose:
                print(f'Skipping archive file {archive_path} because it\'s not a ZIP file!')
            continue
        process_single_ecotaxa_archive(archive_path, num_chunks, output_dir, verbose=verbose)
        print()

if __name__ == '__main__':
    main()
