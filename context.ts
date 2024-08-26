export interface Context {
    /**
     * Associated files, indexed by suffix, selected according to the inheritance principle
     */
    associations: Associations;
    /**
     * TSV columns, indexed by column header, values are arrays with column contents
     */
    columns?: { [key: string]: string[] };
    /**
     * Properties and contents of the entire dataset
     */
    dataset: Dataset;
    /**
     * Datatype of current file, for examples, anat
     */
    datatype?: string;
    /**
     * Entities parsed from the current filename
     */
    entities?: { [key: string]: string };
    /**
     * Extension of current file including initial dot
     */
    extension?: string;
    /**
     * Parsed contents of gzip header
     */
    gzip?: Gzip;
    /**
     * Contents of the current JSON file
     */
    json?: { [key: string]: any };
    /**
     * Modality of current file, for examples, MRI
     */
    modality?: string;
    /**
     * Parsed contents of NIfTI header referenced elsewhere in schema.
     */
    nifti_header?: NiftiHeader;
    /**
     * Parsed contents of OME-XML header, which may be found in OME-TIFF or OME-ZARR files
     */
    ome?: Ome;
    /**
     * Path of the current file
     */
    path: string;
    /**
     * The BIDS specification schema
     */
    schema: { [key: string]: any };
    /**
     * Sidecar metadata constructed via the inheritance principle
     */
    sidecar: { [key: string]: any };
    /**
     * Length of the current file in bytes
     */
    size: number;
    /**
     * Properties and contents of the current subject
     */
    subject?: Subject;
    /**
     * Suffix of current file
     */
    suffix?: string;
    /**
     * TIFF file format metadata
     */
    tiff?: Tiff;
}

/**
 * Associated files, indexed by suffix, selected according to the inheritance principle
 */
export interface Associations {
    /**
     * ASL context file
     */
    aslcontext?: Aslcontext;
    /**
     * B value file
     */
    bval?: Bval;
    /**
     * B vector file
     */
    bvec?: Bvec;
    /**
     * Channels file
     */
    channels?: Channels;
    /**
     * Coordinate system file
     */
    coordsystem?: Coordsystem;
    /**
     * Events file
     */
    events?: Events;
    /**
     * M0 scan file
     */
    m0scan?: M0Scan;
    /**
     * Magnitude image file
     */
    magnitude?: Magnitude;
    /**
     * Magnitude1 image file
     */
    magnitude1?: Magnitude1;
}

/**
 * ASL context file
 */
export interface Aslcontext {
    /**
     * Number of rows in aslcontext.tsv
     */
    n_rows: number;
    /**
     * Path to associated aslcontext file
     */
    path: string;
    /**
     * Contents of the volume_type column
     */
    volume_type?: string[];
}

/**
 * B value file
 */
export interface Bval {
    /**
     * Number of columns in bval file
     */
    n_cols: number;
    /**
     * Number of rows in bval file
     */
    n_rows: number;
    /**
     * Path to associated bval file
     */
    path: string;
    /**
     * B-values contained in bval file
     */
    values: number[];
}

/**
 * B vector file
 */
export interface Bvec {
    /**
     * Number of columns in bvec file
     */
    n_cols: number;
    /**
     * Number of rows in bvec file
     */
    n_rows: number;
    /**
     * Path to associated bvec file
     */
    path: string;
}

/**
 * Channels file
 */
export interface Channels {
    /**
     * Path to associated channels file
     */
    path: string;
    /**
     * Contents of the sampling_frequency column
     */
    sampling_frequency?: string[];
    /**
     * Contents of the short_channel column
     */
    short_channel?: string[];
    /**
     * Contents of the type column
     */
    type?: string[];
}

/**
 * Coordinate system file
 */
export interface Coordsystem {
    /**
     * Path to associated coordsystem file
     */
    path: string;
}

/**
 * Events file
 */
export interface Events {
    /**
     * Contents of the onset column
     */
    onset?: string[];
    /**
     * Path to associated events file
     */
    path: string;
}

/**
 * M0 scan file
 */
export interface M0Scan {
    /**
     * Path to associated M0 scan file
     */
    path: string;
}

/**
 * Magnitude image file
 */
export interface Magnitude {
    /**
     * Path to associated magnitude file
     */
    path: string;
}

/**
 * Magnitude1 image file
 */
export interface Magnitude1 {
    /**
     * Path to associated magnitude1 file
     */
    path: string;
}

/**
 * Properties and contents of the entire dataset
 */
export interface Dataset {
    /**
     * Contents of /dataset_description.json
     */
    dataset_description: { [key: string]: any };
    /**
     * Data types present in the dataset
     */
    datatypes: string[];
    /**
     * Set of ignored files
     */
    ignored: string[];
    /**
     * Modalities present in the dataset
     */
    modalities: string[];
    /**
     * Collections of subjects in dataset
     */
    subjects: Subjects;
    /**
     * Tree view of all files in dataset
     */
    tree: { [key: string]: any };
}

/**
 * Collections of subjects in dataset
 */
export interface Subjects {
    /**
     * The participant_id column of participants.tsv
     */
    participant_id?: string[];
    /**
     * The union of participant_id columns in phenotype files
     */
    phenotype?: string[];
    /**
     * Subjects as determined by sub-* directories
     */
    sub_dirs: string[];
}

/**
 * Parsed contents of gzip header
 */
export interface Gzip {
    /**
     * Comment
     */
    comment?: string;
    /**
     * Filename
     */
    filename?: string;
    /**
     * Modification time, unix timestamp
     */
    timestamp: number;
}

/**
 * Parsed contents of NIfTI header referenced elsewhere in schema.
 */
export interface NiftiHeader {
    /**
     * Data seq dimensions.
     */
    dim: number[];
    /**
     * Metadata about dimensions data.
     */
    dim_info: DimInfo;
    /**
     * NIfTI-MRS JSON fields
     */
    mrs?: { [key: string]: any };
    /**
     * Grid spacings (unit per dimension).
     */
    pixdim: number[];
    /**
     * Use of the quaternion fields.
     */
    qform_code: number;
    /**
     * Use of the affine fields.
     */
    sform_code: number;
    /**
     * Data array shape, equal to dim[1:dim[0] + 1]
     */
    shape: number[];
    /**
     * Voxel sizes, equal to pixdim[1:dim[0] + 1]
     */
    voxel_sizes: number[];
    /**
     * Units of pixdim[1..4]
     */
    xyzt_units: XyztUnits;
}

/**
 * Metadata about dimensions data.
 */
export interface DimInfo {
    /**
     * These fields encode which spatial dimension (1, 2, or 3).
     */
    freq: number;
    /**
     * Corresponds to which acquisition dimension for MRI data.
     */
    phase: number;
    /**
     * Slice dimensions.
     */
    slice: number;
}

/**
 * Units of pixdim[1..4]
 */
export interface XyztUnits {
    /**
     * String representing the unit of inter-volume intervals.
     */
    t: T;
    /**
     * String representing the unit of voxel spacing.
     */
    xyz: Xyz;
}

/**
 * String representing the unit of inter-volume intervals.
 */
export enum T {
    Msec = "msec",
    SEC = "sec",
    Unknown = "unknown",
    Usec = "usec",
}

/**
 * String representing the unit of voxel spacing.
 */
export enum Xyz {
    Meter = "meter",
    Mm = "mm",
    Um = "um",
    Unknown = "unknown",
}

/**
 * Parsed contents of OME-XML header, which may be found in OME-TIFF or OME-ZARR files
 */
export interface Ome {
    /**
     * Pixels / @PhysicalSizeX
     */
    PhysicalSizeX?: number;
    /**
     * Pixels / @PhysicalSizeXUnit
     */
    PhysicalSizeXUnit?: string;
    /**
     * Pixels / @PhysicalSizeY
     */
    PhysicalSizeY?: number;
    /**
     * Pixels / @PhysicalSizeYUnit
     */
    PhysicalSizeYUnit?: string;
    /**
     * Pixels / @PhysicalSizeZ
     */
    PhysicalSizeZ?: number;
    /**
     * Pixels / @PhysicalSizeZUnit
     */
    PhysicalSizeZUnit?: string;
}

/**
 * Properties and contents of the current subject
 */
export interface Subject {
    /**
     * Collections of sessions in subject
     */
    sessions: Sessions;
}

/**
 * Collections of sessions in subject
 */
export interface Sessions {
    /**
     * The union of session_id columns in phenotype files
     */
    phenotype?: string[];
    /**
     * Sessions as determined by ses-* directories
     */
    ses_dirs: string[];
    /**
     * The session_id column of sessions.tsv
     */
    session_id?: string[];
}

/**
 * TIFF file format metadata
 */
export interface Tiff {
    /**
     * TIFF file format version (the second 2-byte block)
     */
    version: number;
}
