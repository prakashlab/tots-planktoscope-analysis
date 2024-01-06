# -*- coding: utf-8 -*-

import csv
import operator

"""Parsing of the ToTS PlanktoScope logsheet."""

_column_names = {
    'src': {
        'id': 'Source Sample ID', # primary key
        'type': 'Sample Type',
        'station_id': 'Station ID (or Local Sampling Timestamp)',
        'cast_id': '(CTD/Net) Cast Number',
        'arrigo_id': '(CTD/Ice/Experiment) Arrigo Number',
        'depth_min': 'Shallowest Depth (m)',
        'depth_max': 'Deepest Depth (m)',
        'start_date_utc': 'Sampling [Start] UTC Date',
        'start_time_utc': 'Sampling [Start] UTC Time',
        'start_lat': 'Sampling [Start] Latitude',
        'start_lon': 'Sampling [Start] Longitude',
    },
    'adj': {
        'id': 'tots-prakash Sample ID', # primary key
        'src_id': 'Source Sample ID',
        'dilution_factor': 'Overall Dilution Factor',
    },
    'acq': {
        'id': 'tots-ps Acquisition ID', # primary key
        'operator': 'Operator',
        'adj_id': 'Adjusted Sample ID',
        'start_time_local': 'Acquisition Start Timestamp (Local Time)',
    },
}

def load(table_files, verbose=False):
    """Loads the logsheet as a joined result of the table in the three files.

    The files should be provided as a dict associating table names to file-like objects of TSV files
    for their respective tables.
    """
    tables = {}
    for table_name, table_file in table_files.items():
        if verbose:
            print(f'Loading table "{table_name}"...')
        tables[table_name] = _extract_columns(_load_table(table_file), _column_names[table_name])
    if verbose:
        print('Joining tables...')
    return _join_tables(tables, _foreign_keys, _primary_table, verbose=verbose)

_tsv_format = {
    'dialect': 'unix',
    'delimiter': '\t',
    'quoting': csv.QUOTE_MINIMAL,
}

def _load_table(tsv_file):
    """Load the specified file-like object containing a TSV table as a list of dicts."""
    reader = csv.DictReader(tsv_file, **_tsv_format)
    rows = [row for row in reader]
    return rows

def _extract_columns(table_rows, column_names):
    """Extracts and renames the specified columns from the table.

    The table should be provided as a list of dicts. The column names should be specified as a dict
    associating desired column names as keys for the original table's column names as values.
    """
    extracted_rows = []
    for row in table_rows:
        extracted_row = {}
        for new_name, old_name in column_names.items():
            extracted_row[new_name] = row[old_name]
        extracted_rows.append(extracted_row)
    return extracted_rows

_foreign_keys = {
    ('acq', 'adj_id'): 'adj',
    ('adj', 'src_id'): 'src',
}
_primary_table = 'acq'

def _join_tables(tables, foreign_keys, primary_table, verbose=False):
    """Joins the provided tables into a single table, starting with the specified primary table/id.

    Tables should be provided as a dict associating table names to lists of table rows (each being
    an object associating column names to values).
    Columns are joined by foreign keys, which should be specified as a dict associating
    (table, column name) pairs of foreign key columns to table names. Each table's primary id column
    is assumed to be named 'id'.
    The primary table should be specified by its table name.

    Returns a list of table rows (each being an object associating (table, column name) pairs to
    values), and an index dict associating the primary key values in the (primary_table, 'id')
    column with array indices in the list of table rows.
    """
    if verbose:
        print('Indexing tables...')
    indices = {}
    for table_name, rows in tables.items():
        if table_name == primary_table:
            continue
        indices[table_name] = _index_table(rows, id_column='id')

    if verbose:
        print(f'Joining starting with table "{primary_table}"...')
    root = tables[primary_table]
    joined_rows = []
    for row in tables[primary_table]:
        joined_row = {}
        _copy_join_columns(joined_row, primary_table, row)
        joined_rows.append(joined_row)

    remaining = dict(_foreign_keys)
    while len(remaining) > 0:
        for reference, referent_table in remaining.items():
            if reference not in joined_rows[0]:
                # The foreign key hasn't yet been added to the joined table,
                # so we'll skip it for now and try again later
                continue
            # We found a resolvable foreign key!
            break
        else:
            # We couldn't resolve any more foreign keys
            raise ValueError(f'Couldn\'t resolve remaining foreign keys: {remaining}')

        del remaining[reference]
        if verbose:
            print(f'Resolving foreign key {reference} => ({referent_table}, \'id\')...')
        index = indices[referent_table]
        for joined_row in joined_rows:
            resolved_row = tables[referent_table][index[joined_row[reference]]]
            del joined_row[reference]
            _copy_join_columns(joined_row, referent_table, resolved_row)

    return joined_rows, _index_table(joined_rows, id_column=(primary_table, 'id'))

def _index_table(rows, id_column='id'):
    """Build an index of a table's rows by its id column.

    Returns a dict associating table IDs with row indices.

    The table is provided as a list of dicts, each of which should have an 'id' key.
    """
    index = {}
    for i, row in enumerate(rows):
        if row[id_column] in index:
            raise KeyError(f'Duplicate id {row[id_column]} found!')
        index[row[id_column]] = i
    return index

def _copy_join_columns(joined_row, source_table_name, source_row):
    """Adds the columns from the specified source table's specified row to the joined row.

    Column names are (source_table_name, column) pairs.
    """
    for column, value in source_row.items():
        joined_row[(source_table_name, column)] = value
