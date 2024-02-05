# -*- coding: utf-8 -*-
"""Handling of PlanktoScope ecotaxa metadata tables"""

import csv

_tsv_format = {
    'dialect': 'unix',
    'delimiter': '\t',
    'quoting': csv.QUOTE_MINIMAL,
}

def read_file(metadata_file):
    """Load the rows of a TSV file containing EcoTaxa object metadata, as a list of dicts per row.

    Returns the first row of the file (containing numpy format specifiers) separately from the rows
    containing actual data.

    The cursor of the table file must be at the appropriate location before the function is called,
    and it is left at the end of the file when the function returns.
    """
    reader = csv.DictReader(metadata_file, **_tsv_format)
    rownum = 0
    field_types = {}
    data_rows = []
    for row in reader:
        if rownum == 0:
            field_types = row
            rownum += 1
            continue
        data_rows.append(row)
    return (field_types, data_rows)

def write_file(output_metadata_file, field_types, data_rows):
    """Write the EcoTaxa object metadata to a TSV file.

    The cursor of the table file must be at the appropriate location before the function is called,
    and it is left at the end of the file when the function returns.
    """
    writer = csv.DictWriter(output_metadata_file, field_types.keys(), **_tsv_format)
    writer.writeheader()
    writer.writerow(field_types)
    for row in data_rows:
        writer.writerow(row)
