#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Command line utility for generating metadata corrections from the ToTS PlanktoScope logsheet."""

import argparse
import io
import json
import math
import os
import tempfile

from . import ecotaxa
from . import tables

def main():
    """Generate EcoTaxa metadata corrections from the specified ToTS PlanktoScope logsheet."""
    parser = argparse.ArgumentParser(
        prog='logsheet-corrections-generate',
        description='Generate EcoTaxa metadata correction files',
    )
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
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        default=False,
        help='Print additional information for troubleshooting',
    )
    args = parser.parse_args()
    logsheet_table_files = {
        'src': args.logsheet_src,
        'adj': args.logsheet_adj,
        'acq': args.logsheet_acq,
    }
    generate_corrections(
        logsheet_table_files, args.acq_id, args.output, verbose=args.verbose,
    )

def generate_corrections(
    logsheet_table_files, acq_id, output_file, verbose=False,
):
    """Generate a metadata corrections file for the specified image acquisition from the logsheet.

    The logsheet should be provided as a dict associating table names to file-like objects of TSV
    files for their respective tables.
    """
    if verbose:
        print('Loading log sheet from:')
        for table_name, file in logsheet_table_files.items():
            print(f'  {table_name}: {file.name}')
    joined_rows, index = tables.load(logsheet_table_files, verbose=verbose)

    if verbose:
        print(f'Generating corrections for {acq_id}...')
    corrections = ecotaxa.generate_corrections(joined_rows[index[acq_id]], verbose=verbose)
    if verbose:
        print(f'Corrections for {acq_id}:')
        for field, value in corrections.items():
            print(f'  - {field}: {value}')
        print(f'Writing corrections to {output_file.name}...')
    json.dump(corrections, output_file, indent=2)

if __name__ == '__main__':
    main()
