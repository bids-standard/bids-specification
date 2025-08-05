from bidsschematools.types import context as ctx
from bidsschematools.types import protocols as p


def test_import():
    "Verify that the module contains the generated content."
    assert ctx.__doc__ is not None
    assert ctx.__doc__.splitlines()[0].startswith("BIDS validation context")
    assert "Context" in ctx.__all__

    assert isinstance(ctx.Context, type)


def test_assignability() -> None:
    """Verify that dataclass values can be assigned to variables annotated with protocols.

    For pytest, this just checks instantiability.
    Running mypy with bst installed should check assignability,
    for example, with::

        uvx --with=. mypy tests
    """
    subjects: p.Subjects = ctx.Subjects([])
    subjects = ctx.Subjects([], [])

    dataset: p.Dataset = ctx.Dataset(
        dataset_description={},
        tree={},
        ignored=[],
        datatypes=[],
        modalities=[],
        subjects=subjects,
    )

    magnitude: p.Magnitude = ctx.Magnitude("path")
    magnitude1: p.Magnitude1 = ctx.Magnitude1("path")
    m0scan: p.M0scan = ctx.M0scan("path")
    bval: p.Bval = ctx.Bval("path", 5, 1, [0, 0, 0, 0, 0])
    channels: p.Channels = ctx.Channels("path")
    channels = ctx.Channels("path", ["TYPE"], ["1"], ["SHORT"])
    events: p.Events = ctx.Events("path", ["0.0", "3.0"])
    bvec: p.Bvec = ctx.Bvec("path", 5, 3)
    coordsystem: p.Coordsystem = ctx.Coordsystem("path")
    aslcontext: p.Aslcontext = ctx.Aslcontext("path", 2, ["label", "control"])
    associations: p.Associations = ctx.Associations()
    associations = ctx.Associations(
        magnitude=magnitude,
        magnitude1=magnitude1,
        m0scan=m0scan,
        bval=bval,
        channels=channels,
        events=events,
        bvec=bvec,
        coordsystem=coordsystem,
        aslcontext=aslcontext,
    )

    gzip: p.Gzip = ctx.Gzip(0)
    gzip = ctx.Gzip(0, "filename", "comment")

    sessions: p.Sessions = ctx.Sessions([])
    sessions = ctx.Sessions([], [])
    subject: p.Subject = ctx.Subject(sessions)

    tiff: p.Tiff = ctx.Tiff(0x4D4D)

    dim_info: p.DimInfo = ctx.DimInfo(1, 2, 3)
    xyzt_units: p.XyztUnits = ctx.XyztUnits("mm", "sec")
    nifti_header: p.NiftiHeader = ctx.NiftiHeader(
        dim_info=dim_info,
        dim=[4, 64, 64, 48, 100, 1, 1, 1],
        pixdim=[1.0, 1.0, 1.0, 1.0, 1.5, 1.0, 1.0, 1.0],
        shape=(64, 64, 48, 100),
        voxel_sizes=(1.0, 1.0, 1.0, 1.5),
        xyzt_units=xyzt_units,
        qform_code=1,
        sform_code=1,
        axis_codes=("L", "P", "S"),
    )

    ome: p.Ome = ctx.Ome()
    ome = ctx.Ome(
        PhysicalSizeX=10,
        PhysicalSizeY=10,
        PhysicalSizeZ=10,
        PhysicalSizeXUnit="um",
        PhysicalSizeYUnit="um",
        PhysicalSizeZUnit="um",
    )

    context: p.Context = ctx.Context(
        schema={},
        dataset=dataset,
        path="path",
        size=0,
        sidecar={},
        associations=associations,
    )
    context = ctx.Context(
        schema={},
        dataset=dataset,
        subject=subject,
        path="path",
        modality="modality",
        datatype="datatype",
        entities={},
        suffix="suffix",
        extension=".ext",
        size=0,
        sidecar={},
        associations=associations,
        gzip=gzip,
        tiff=tiff,
        ome=ome,
        nifti_header=nifti_header,
        columns={},
        json={},
    )
    assert context.schema == {}  # Use the variable to pacify linters
