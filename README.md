# tots-planktoscope-analysis

Data QC/analysis scripts for PlanktoScope datasets in the ToTS project

This repository contains various scripts used for pre/post-processing PlanktoScope datasets before/after they are annotated on EcoTaxa. This includes fixing various missing or incorrect values in the dataset metadata.

## Usage

To use these tools, it's recommended to [install pipx](https://pypa.github.io/pipx/) and then use pipx to install the tools, via the following command in your terminal:

```
pipx install git+https://github.com/prakashlab/tots-planktoscope-analysis.git
```

Then you can run the `ecotaxa-metadata-edit` tool (for modifying the metadata of a single dataset to fix incorrect/missing values) in your terminal as:

```
ecotaxa-metadata-edit
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
