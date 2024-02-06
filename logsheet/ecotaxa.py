# -*- coding: utf-8 -*-

_ecotaxa_column_mappings = { # these map EcoTaxa export field names to log sheet columns
    None: { # these mappings are used for all sample types
        'sample_id': ('src', 'arrigo_id'),
        'sample_operator': ('acq', 'operator'),
        'object_date': ('src', 'start_date_utc'),
        'object_time': ('src', 'start_time_utc'),
        'object_lat': ('src', 'start_lat'),
        'object_lon': ('src', 'start_lon'),
        'object_depth_min': ('src', 'depth_min'),
        'object_depth_max': ('src', 'depth_max'),
        'acq_id': ('acq', 'acq_id'),
        'acq_local_datetime': ('acq', 'start_time_local'),
    },
    # sample type-specific mappings are applied afterwards and can overwrite general mappings
}

_ecotaxa_corrections = { # these define values to change EcoTaxa export field values to
    None: { # these corrections are used for all sample types
        'sample_sampling_gear': 'single_location',
    },
    # sample type-specific corrections are applied afterwards and can overwrite general corrections
}

def generate_corrections(row, verbose=False):
    corrections = {}
    for ecotaxa_field, column_name in _ecotaxa_column_mappings[None].items():
        corrections[ecotaxa_field] = row[column_name]
    sample_type = row[('src', 'type')]
    if sample_type in _ecotaxa_column_mappings:
        for ecotaxa_field, column_name in _ecotaxa_column_mappings[sample_type].items():
            corrections[ecotaxa_field] = row[column_name]
    for ecotaxa_field, value in _ecotaxa_corrections[None].items():
        corrections[ecotaxa_field] = value
    if sample_type in _ecotaxa_corrections:
        for ecotaxa_field, value in _ecotaxa_corrections[sample_type].items():
            corrections[ecotaxa_field] = value
    return corrections

