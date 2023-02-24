# Computational Models

Support for the modality `comp` was developed as a
[BIDS Extension Proposal](https://docs.google.com/document/d/1NT1ERdL41oz3NibIFRyVQ2iR8xH-dKY-lRCB4eyVeRo/edit#heading=h.mqkmyp254xh6).

BIDS Computational Model files store the mathematical and computational descriptions of
computational models as well as simulation results.
To ensure that computational modelling results are reproducible it is necessary to store
for every simulation result the used

-   mathematical model equations (including all state variables and generic parameters),
-   specific parameter settings (for example, for a certain `sub`, `ses`, `task`, ...)
-   structural connectivity
-   source code
-   and machine code.

Therefore, every file that contains computational model simulation results **MUST**
reference these files in a JSON sidecar file.

To store code either the modality agnostic datatype `code` or publicly accessible
long-term repositories can be used. To store models the datatype `model` **MUST** be
used.

**Caveat**: To store structural connectivity the datatype `connectivity` developed in
[BEP017](https://docs.google.com/document/d/1ugBdUF6dhElXdj3u9vw0iWjE6f_Bibsro3ah7sRV0GA/edit#)
is planned to be used.
To store simulation results a new datatype for storing time series will be needed.
The need for such a BIDS-wide datatype to store time series was
[identified](https://github.com/bids-standard/bids-specification/issues/713).

The following filetree exemplifies the directory structure.

{{ MACROS___make_filetree_example(

{
    	"comp": {
    		"model": {
    			"desc-Generic2dOscillator_eq.xml": "                     generic equations for all subjects",
    			"desc-JansenRit_eq.xml": "",
    			"desc-JansenRit-healthy_param.xml": "                    generic parameters for all subjects",
    			"desc-Generic2dOscillator-healthy_param.xml": "",
    		},
    		"code": {
    			"desc-Generic2dOscillator-script.py": "                  generic machine code for all subjects",
    			"desc-JansenRit.img": "",
    			"desc-JansenRit-Dockerfile.txt": "                       generic source code for all subjects"
    		},
    		"sub-01": {
    			"model": {
    				"sub-01_desc-JansenRit-stroke_param.xml": "           subject-specific parameters only for sub-01",
    				"sub-01_desc-Generic2dOscillator-stroke_param.xml": ""
    			},
    			"code": {
    				"sub-01_desc-preproc.py": "                           subject-specific code only for sub-01"
    			},
    			"timeseries": {
    				"sub-01_desc-testsim.tsv": "                          Datatype timeseries not yet existing, but needed: <https://github.com/bids-standard/bids-specification/issues/713>",
    				"sub-01_desc-testsim.json": "                         every simulation result has a JSON sidecar that references the used model, code and connectivity",
    				"sub-01_task-motor.tsv": "",
    				"sub-01_task-motor.json": "",
    				"sub-01_task-motor_desc-burnin.tsv": "",
    				"sub-01_task-motor_desc-burnin.json": ""
    			},
    			"connectivity": {
    				"sub-01_conndata-network_connectivity.tsv": "         as per BEP017: connectivity data schema",
    				"sub-01_conndata-network_connectivity.json": ""
    			}
    		}
    	}
}

) }}

## Datatype: `model`

{{ MACROS___make_filename_template(datatypes=["model"], suffixes=["eq", "param"]) }}

Equations and parameters **MUST** be specified using the XML-based
[**L**ow **E**ntropy **M**odel **S**pecification (LEMS)](http://lems.github.io/LEMS)
format.
LEMS provides a compact, minimally redundant, human-readable, human-writable, declarative
way of expressing models of physical systems.
[PyLEMS](https://github.com/LEMS/pylems) is a Python implementation of the LEMS language
that can both parse and simulate existing LEMS models and provides an API in Python for
reading, modifying and writing LEMS files.
See the
[original publication introducing LEMS](https://pubmed.ncbi.nlm.nih.gov/25309419/),
and its [repository](http://lems.github.io/LEMS) with examples for more information.
A basic principle of LEMS is to separate equations and parameter settings such that the
equations need only be stated once and can then be reused with different
parameterizations.

### Entity: model equations (suffix: `"_eq.xml"`)

Every simulation result MUST link to the used equations in LEMS-formatted `*_eq.xml` files
using the metadata keyword `"ModelEq"`.

### Entity: model parameters (suffix: `"_param.xml"`)

Every simulation result MUST link to the used parameter settings in LEMS-formatted
`*_param.xml` files using the keyword `"ModelParam"`.

## Datatype: `code`

Code involves

-   "source code" (human-readable standard programming language)

-   and "machine code" (executable program; in the case of an interpreted language like
    Python, machine code and source code may be identical).

Every BIDS dataset that contains simulation results **MUST** either directly store the
**source code** and the **executable machine code** that was used to produce the result in
the
[modality agnostic directory code](https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#code)
or in a publicly accessible long-term repository.
Every BIDS file that contains a simulation result **MUST** have a JSON sidecar file that
links to the location of the used codes (either using URIs or relative file paths in the
BIDS data set) using the metadata keys `"SourceCodeRepository"` and
`"MachineCodeRepository"`.

It is preferred that machine code exist in the form of self-contained container images
(including the entire necessary computational environment).

## Metadata

**Note**: currently there is no datatype for simulation results in BIDS. There are
however efforts towards a datatype to store
[time series](https://github.com/bids-standard/bids-specification/issues/713),
which may then be accompanied by JSON sidecar files with the entities below.
Furthermore, connectivity information must be referenced using the entity
`"Connectivity"`, support for which is currently developed in
[BEP017](https://docs.google.com/document/d/1ugBdUF6dhElXdj3u9vw0iWjE6f_Bibsro3ah7sRV0GA/edit#)

{{ MACROS___make_metadata_table(
{
"SourceCodeRepository": "REQUIRED",
"MachineCodeRepository": "REQUIRED",
"ModelEq": "REQUIRED",
"ModelParam": "REQUIRED",
"Connectivity": "REQUIRED"
}
) }}
