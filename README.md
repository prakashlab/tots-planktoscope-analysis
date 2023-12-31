# tots-planktoscope-analysis

Data QC/analysis scripts for PlanktoScope datasets in the ToTS project

This repository contains various scripts used for pre/post-processing PlanktoScope datasets before/after they are annotated on EcoTaxa. This includes fixing various missing or incorrect values in the dataset metadata.

## Usage

To use these tools, it's recommended to [install pipx](https://pypa.github.io/pipx/) and then use pipx to install the tools, via the following command in your terminal:

```
pipx install git+https://github.com/prakashlab/tots-planktoscope-analysis.git
```

### Generate corrections

To generate a corrections file for a single image acquisition dataset, you can run the `logsheet-corrections-generate` command using:

```
logsheet-corrections-generate single \
  <path to TSV file for the sample sources table of the log sheet> \
  <path to TSV file for the sample adjustments table of the log sheet> \
  <path to TSV file for the image acquisitions table of the log sheet> \
  <image acquisition dataset ID>
  <path to JSON file to save corrections to>
```

For example:

```
logsheet-corrections-generate single \
  ./log-sheet-snapshots/2024-01-08/src.tsv \
  ./log-sheet-snapshots/2024-01-08/adj.tsv \
  ./log-sheet-snapshots/2024-01-08/acq.tsv \
  tots-ps-acq-228 \
  ./corrections/tots-ps-acq-228.json
```

To instead generate corrections files for all image acquisition datasets in a logsheet, you can instead run the `logsheet-corrections-generate` command using:

```
logsheet-corrections-generate batch \
  <path of directory with TSV files for the tables of the log sheet> \
  <path of directory to save corrections to as JSON files>
```

For example:

```
logsheet-corrections-generate batch ./log-sheet-snapshots/2024-01-08/ ./corrections/
```

### Apply corrections

To apply a corrections file for a single image acquisition dataset, you can run the `ecotaxa-metadata-edit` command using:

```
ecotaxa-metadata-edit single \
  <path to results archive> \
  <path to JSON file for the corrections for the dataset> \
  <path to ZIP file to save the corrected EcoTaxa export archive as> \
  <path to JSON file to record changes to>
```

For example:

```
ecotaxa-metadata-edit single \
  ../tots-ps/data/tots-ps-acq-228-results.tar.gz \
  ./corrections/tots-ps-acq-228.json \
  ../tots-ps/analysis/tots-ps-acq-228-export.zip \
  ./changes/tots-ps-acq-228.json
```

To instead apply all corrections files in a directory for all results archives in a directory, you can instead run the `ecotaxa-metadata-edit` command using:

```
ecotaxa-metadata-edit batch \
  <path of directory with results archives> \
  <path of directory with metadata corrections files> \
  <path of directory to save corrected EcoTaxa export archives to> \
  <path of directory to save changes records to>
```

For example:

```
ecotaxa-metadata-edit batch ../tots-ps/data/ ./corrections/ ../tots-ps/analysis/ ./changes/
```

## Contributing

Currently, this project does not accept any outside contributions.

## Licensing

I have chosen the following licenses in order to give away this work for free, so that you can freely use it for whatever purposes you have, with minimal restrictions while still protecting my disclaimer that this work is provided without any warranties at all.

### Software

Except where otherwise indicated in this repository, software files provided here are covered by the following information:

**Copyright Ethan Li**

SPDX-License-Identifier: `Apache-2.0 OR BlueOak-1.0.0`

Software files in this project are released under the [Apache License v2.0](https://www.apache.org/licenses/LICENSE-2.0) and the [Blue Oak Model License 1.0.0](https://blueoakcouncil.org/license/1.0.0); you can use the source code provided here under the Apache License or under the Blue Oak Model License, and you get to decide which license you will agree to. I am making the software available under the Apache license because it's [OSI-approved](https://writing.kemitchell.com/2019/05/05/Rely-on-OSI.html) and it goes well together with the [Solderpad Hardware License](https://solderpad.org/licenses/SHL-2.1/), which is an open hardware license used in various projects I have worked on; but I like the Blue Oak Model License more because it's easier to read and understand. Please read and understand the licenses for the specific language governing permissions and limitations.

### Everything else

Except where otherwise indicated in this repository, any other files (such as images, media, data, and textual documentation) provided here not already covered by software or hardware licenses (described above) are instead covered by the following information:

**Copyright Ethan Li**

SPDX-License-Identifier: `CC-BY-4.0`

Files in this project are released under the [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/). Please read and understand the license for the specific language governing permissions and limitations.
