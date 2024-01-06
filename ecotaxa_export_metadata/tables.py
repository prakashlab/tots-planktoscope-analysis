# -*- coding: utf-8 -*-
"""Handling of table-structured data in the ToTS project"""

import collections
import csv

_ecotaxa_tsv_format = {
    'dialect': 'unix',
    'delimiter': '\t',
    'quoting': csv.QUOTE_MINIMAL,
}

def rewrite_ecotaxa_metadata(table_file, overrides, verbose=False):
    """Rewrite columns of the EcoTaxa object metadata TSV file based on the dict of overrides.

    The cursor of the table file must be at the appropriate location before the function is called,
    and it is left at the end of the file."""
    field_types, data_rows = _read_ecotaxa_metadata(table_file)
    if verbose:
        print(f'Number of objects: {len(data_rows)}')
    updated_fields = _rewrite_row_fields(data_rows, overrides)
    if verbose:
        print('Updated fields and previous values:')
        for field, old_values in updated_fields.items():
            print(f'  - {field}: {", ".join(sorted(list(old_values)))}')
    table_file.seek(0)
    table_file.truncate()
    _write_ecotaxa_metadata(table_file, field_types, data_rows)

def _read_ecotaxa_metadata(table_file):
    """Load the rows of a TSV file containing EcoTaxa object metadata, as a list of dicts per row.

    Returns the first row of the file (containing numpy format specifiers) separately from the rows
    containing actual data.

    The cursor of the table file must be at the appropriate location before the function is called,
    and it is left at the end of the file when the function returns.
    """
    reader = csv.DictReader(table_file, **_ecotaxa_tsv_format)
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

def _rewrite_row_fields(data_rows, overrides):
    """Update the values of certain fields of each row based on the dict of overrides."""
    updated_columns = collections.defaultdict(set)
    for row in data_rows:
        for (key, value) in overrides.items():
            old_value = row[key]
            if old_value != value:
                updated_columns[key].add(old_value)
                row[key] = value
    return updated_columns

def _write_ecotaxa_metadata(table_file, field_types, data_rows):
    """Write the EcoTaxa object metadata to a TSV file.

    The cursor of the table file must be at the appropriate location before the function is called,
    and it is left at the end of the file when the function returns.
    """
    writer = csv.DictWriter(table_file, field_types.keys(), **_ecotaxa_tsv_format)
    writer.writeheader()
    writer.writerow(field_types)
    for row in data_rows:
        writer.writerow(row)
