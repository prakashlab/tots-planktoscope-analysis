#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Command line utility for generating metadata corrections from the ToTS PlanktoScope logsheet."""

import argparse
import io
import json
import math
import os
import pathlib
import tempfile

from . import ecotaxa
from . import tables

def main():
    """Generate EcoTaxa metadata corrections from the specified ToTS PlanktoScope logsheet(s)."""
    parser = argparse.ArgumentParser(
        prog='logsheet-corrections-generate',
        description='Generate EcoTaxa metadata correction files',
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
    """Set up a (sub)parser to generate corrections for a single ToTS PlanktoScope dataset."""
    parser.add_argument(
        'logsheet_src',
        type=argparse.FileType(mode='r'),
        help='Path of a TSV file of the PlanktoScope logsheet\'s source samples table to load',
    )
    parser.add_argument(
        'logsheet_adj',
        type=argparse.FileType(mode='r'),
        help='Path of a TSV file of the PlanktoScope logsheet\'s sample adjustments table to load',
    )
    parser.add_argument(
        'logsheet_acq',
        type=argparse.FileType(mode='r'),
        help='Path of a TSV file of the PlanktoScope logsheet\'s image acquisitions table to load',
    )
    parser.add_argument(
        'acq_id',
        type=str,
        help='tots-ps acquisition ID of the acquisition to generate a metadata correction file for',
    )
    parser.add_argument(
        'output',
        type=argparse.FileType(mode='w'),
        help='Path of the EcoTaxa metadata corrections JSON file to create',
    )
    parser.set_defaults(func=lambda args: generate_single_corrections(
        args.logsheet_src, args.logsheet_adj, args.logsheet_acq,
        args.acq_id, args.output, verbose=args.verbose,
    ))

def generate_single_corrections(
    logsheet_src_file, logsheet_adj_file, logsheet_acq_file, acq_id, output_file, verbose=False,
):
    """Generate a metadata corrections file for the specified acquisition, based on the logsheet.

    The logsheet should be provided as a dict associating table names to file-like objects of TSV
    files for their respective tables.
    """
    logsheet_files = {
        'src': logsheet_src_file,
        'adj': logsheet_adj_file,
        'acq': logsheet_acq_file,
    }
    if verbose:
        print('Loading log sheet from:')
        for table_name, file in logsheet_files.items():
            print(f'  {table_name}: {file.name}')
    joined_rows, index = tables.load(logsheet_files, verbose=verbose)

    if verbose:
        print(f'Generating corrections for {acq_id}...')
    corrections = ecotaxa.generate_corrections(joined_rows[index[acq_id]], verbose=verbose)
    if verbose:
        print(f'Corrections for {acq_id}:')
        for field, value in corrections.items():
            print(f'  - {field}: {value}')
        print(f'Writing corrections to {output_file.name}...')
    json.dump(corrections, output_file, indent=2)

# batch subcommand

def setup_batch_parser(parser):
    """Set up a (sub)parser to generate corrections for multiple ToTS PlanktoScope datasets."""
    parser.add_argument(
        'logsheet',
        type=str,
        help='Directory of TSV files of the PlanktoScope logsheet\'s tables to load',
    )
    parser.add_argument(
        'output',
        type=str,
        help='Directory in which to create EcoTaxa metadata corrections JSON files',
    )
    parser.set_defaults(func=lambda args: generate_all_corrections(
        args.logsheet, args.output, verbose=args.verbose,
    ))

def generate_all_corrections(logsheet_dir, output_dir, verbose=False):
    """Generate a metadata corrections file for each acquisition in the logsheet.

    The logsheet should be provided as the path of a directory of TSV files for their respective
    tables in the logsheet. The name of each table should be `{tablename}.tsv`.
    """
    # Load logsheet
    logsheet_files = {}
    for file_path in os.listdir(logsheet_dir):
        parsed_path = pathlib.Path(logsheet_dir).joinpath(file_path)
        if not parsed_path.suffix == '.tsv':
            if verbose:
                print(f'Skipping log-sheet file {file_path} because it\'s not a TSV file!')
            continue
        file = open(parsed_path, 'r') # we rely on CPython to close open files upon completion
        logsheet_files[parsed_path.stem] = file
    if verbose:
        print('Loading log sheet from:')
        for table_name, file in logsheet_files.items():
            print(f'  {table_name}: {file.name}')
    joined_rows, index = tables.load(logsheet_files, verbose=verbose)

    # Generate corrections for each acquisition in the logsheet
    for acq_id in index.keys():
        if verbose:
            print(f'Generating corrections for {acq_id}...')
        corrections = ecotaxa.generate_corrections(joined_rows[index[acq_id]], verbose=verbose)
        if verbose:
            print(f'Corrections for {acq_id}:')
            for field, value in corrections.items():
                print(f'  - {field}: {value}')
        output_path = pathlib.Path(output_dir).joinpath(acq_id + '.json')
        with open(output_path, 'w') as output_file:
            if verbose:
                print(f'Writing corrections to {output_file.name}...')
            json.dump(corrections, output_file, indent=2)

if __name__ == '__main__':
    main()
