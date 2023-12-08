#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Command line utilities for editing metadata in EcoTaxa export archives"""

import argparse


def main():
    """Utilities for Iridium message parsing."""
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
    args = parser.parse_args()
    print('Hello, world!')


if __name__ == '__main__':
    main()
