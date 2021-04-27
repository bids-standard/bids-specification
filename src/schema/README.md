# BIDS-schema

Portions of the BIDS specification are defined using YAML files, in order to
make the specification machine-readable.

Currently, the only portion of the specification that relies on this schema is
the Entity Table, but any changes to the specification should be mirrored in the
schema.

## The format of the schema

The schema reflects the files and objects in the specification, as well as
associations between these objects. Here is a list of the files and subfolders
of the schema, roughly in order of importance:

-   `datatypes/*.yaml`: Data types supported by the specification. Each datatype
    may support many suffixes. These suffixes are divided into groups based on
    what extensions and entities are allowed for each. Data types correspond to
    subfolders (for example, `anat`, `func`) in the BIDS structure.
    
-   `entities.yaml`: A list of entities (key/value pairs in folder and
    filenames) with associated descriptions and formatting rules. The order of
    the entities in the file determines the order in which entities must appear
    in filenames.

-   `top_level_files.yaml`: Modality-agnostic files stored at the top level of a
    BIDS dataset. The schema specifies whether these files are required or
    optional, as well as acceptable extensions for each.
    
-   `modalities.yaml`: Modalities supported by the specification, along with a
    list of associated data types. Modalities are not reflected directly in the
    BIDS structure, but data types are modality-specific.
    
-   `associated_data.yaml`: Folders that are commonly contained within the same
    folder as a BIDS dataset, but which do not follow the BIDS structure
    internally, such as `code` or `sourcedata`. The schema specifies which
    folders are accepted and whether they are required or optional.
