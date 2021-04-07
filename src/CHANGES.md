# Changelog

## [Unreleased](https://github.com/bids-standard/bids-specification/tree/HEAD)

-   \[INFRA] install git in linkchecker job [#767](https://github.com/bids-standard/bids-specification/pull/767) ([sappelhoff](https://github.com/sappelhoff))
-   \[INFRA] Fix CircleCI workflows [#764](https://github.com/bids-standard/bids-specification/pull/764) ([sappelhoff](https://github.com/sappelhoff))
-   \[INFRA] do not run remark on auto CHANGES [#755](https://github.com/bids-standard/bids-specification/pull/755) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] Mix up (typo) between ficiduals and landmarks in EEG spec [#754](https://github.com/bids-standard/bids-specification/pull/754) ([rob-luke](https://github.com/rob-luke))
-   \[INFRA] updating remark, CIs, contributor docs [#745](https://github.com/bids-standard/bids-specification/pull/745) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] schema for i/eeg coordsys+elecs: sub-ses-acq-space are allowed entities [#743](https://github.com/bids-standard/bids-specification/pull/743) ([sappelhoff](https://github.com/sappelhoff))
-   \[DOC] move schema documentation into the schema folder [#740](https://github.com/bids-standard/bids-specification/pull/740) ([Remi-Gau](https://github.com/Remi-Gau))
-   \[MISC] standardize string examples format in tables [#739](https://github.com/bids-standard/bids-specification/pull/739) ([Remi-Gau](https://github.com/Remi-Gau))
-   \[MISC] Clarify participant_id in participants.tsv file if it exists [#738](https://github.com/bids-standard/bids-specification/pull/738) ([adam2392](https://github.com/adam2392))
-   \[FIX] split MEG files should be listed separately in scans.tsv [#735](https://github.com/bids-standard/bids-specification/pull/735) ([eort](https://github.com/eort))
-   \[FIX] 1) Clarify appropriate labels for space entity, 2) Clarify channels+electrodes do not have to match [#734](https://github.com/bids-standard/bids-specification/pull/734) ([sappelhoff](https://github.com/sappelhoff))

## [v1.5.0](https://github.com/bids-standard/bids-specification/tree/v1.5.0) (2021-02-23)

-   Updated TotalAcquiredVolumes into TotalAcquiredPairs [#742](https://github.com/bids-standard/bids-specification/pull/742) ([effigies](https://github.com/effigies))
-   REL: v1.5.0 [#736](https://github.com/bids-standard/bids-specification/pull/736) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[SCHEMA] Update qMRI fieldmap schema [#728](https://github.com/bids-standard/bids-specification/pull/728) ([effigies](https://github.com/effigies))
-   \[FIX] Add deprecated anatomical MRI suffixes back into schema [#725](https://github.com/bids-standard/bids-specification/pull/725) ([tsalo](https://github.com/tsalo))
-   \[FIX] Correct schema irregularities for func datatype [#724](https://github.com/bids-standard/bids-specification/pull/724) ([tsalo](https://github.com/tsalo))
-   \[FIX] Make flip optional for MP2RAGE [#722](https://github.com/bids-standard/bids-specification/pull/722) ([tsalo](https://github.com/tsalo))
-   \[FIX] Correct entity names in YAML files [#720](https://github.com/bids-standard/bids-specification/pull/720) ([tsalo](https://github.com/tsalo))
-   \[ENH] Clarify run indexing information for MRI acquisitions [#719](https://github.com/bids-standard/bids-specification/pull/719) ([effigies](https://github.com/effigies))
-   \[ENH] Harmonize CoordinateSystem details for MRI, MEG, EEG, iEEG [#717](https://github.com/bids-standard/bids-specification/pull/717) ([sappelhoff](https://github.com/sappelhoff))
-   \[SCHEMA] Update entity YAML keys [#714](https://github.com/bids-standard/bids-specification/pull/714) ([effigies](https://github.com/effigies))
-   \[MISC] Added full names for some contributors in .mailmap file [#705](https://github.com/bids-standard/bids-specification/pull/705) ([yarikoptic](https://github.com/yarikoptic))
-   \[INFRA] Migrate md and yml checks from travis to GH actions [#693](https://github.com/bids-standard/bids-specification/pull/693) ([sappelhoff](https://github.com/sappelhoff))
-   \[INFRA] Move part entity to before recording entity [#692](https://github.com/bids-standard/bids-specification/pull/692) ([tsalo](https://github.com/tsalo))
-   \[ENH] BEP001 - qMRI maps and some additional metadata [#690](https://github.com/bids-standard/bids-specification/pull/690) ([agahkarakuzu](https://github.com/agahkarakuzu))
-   \[ENH] BEP001 - Entity-linked file collections [#688](https://github.com/bids-standard/bids-specification/pull/688) ([effigies](https://github.com/effigies))
-   \[ENH] BEP001 - New entities: inv & mt [#681](https://github.com/bids-standard/bids-specification/pull/681) ([agahkarakuzu](https://github.com/agahkarakuzu))
-   \[DOC] add contributing guidelines to add figures in the specs [#679](https://github.com/bids-standard/bids-specification/pull/679) ([Remi-Gau](https://github.com/Remi-Gau))
-   \[MISC] use RFC 2119 language in legend of the "volume timing" table [#678](https://github.com/bids-standard/bids-specification/pull/678) ([Remi-Gau](https://github.com/Remi-Gau))
-   \[FIX] Add OPTIONAL acq entity to channels.tsv, events.tsv to match electrophysiological acquisitions [#677](https://github.com/bids-standard/bids-specification/pull/677) ([sappelhoff](https://github.com/sappelhoff))
-   \[MISC] Update all links to use HTTPS whenever possible. [#676](https://github.com/bids-standard/bids-specification/pull/676) ([gllmflndn](https://github.com/gllmflndn))
-   \[INFRA] Relax line length limit for linting YAML files [#673](https://github.com/bids-standard/bids-specification/pull/673) ([effigies](https://github.com/effigies))
-   \[ENH] BEP001 - New entity: flip [#672](https://github.com/bids-standard/bids-specification/pull/672) ([agahkarakuzu](https://github.com/agahkarakuzu))
-   \[ENH] BEP001 - RepetitionTimeExcitation and RepetitionTimePreparation [#671](https://github.com/bids-standard/bids-specification/pull/671) ([agahkarakuzu](https://github.com/agahkarakuzu))
-   \[ENH] Bep 005: Arterial Spin Labeling [#669](https://github.com/bids-standard/bids-specification/pull/669) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] Added white space after table [#660](https://github.com/bids-standard/bids-specification/pull/660) ([robertoostenveld](https://github.com/robertoostenveld))
-   \[MISC] add remi as maintainer [#657](https://github.com/bids-standard/bids-specification/pull/657) ([Remi-Gau](https://github.com/Remi-Gau))
-   \[MISC] update Contributing with info on how to respond to reviews [#655](https://github.com/bids-standard/bids-specification/pull/655) ([Remi-Gau](https://github.com/Remi-Gau))
-   \[FIX] add paragraph on MEG specific "markers" suffix in MEG spec [#653](https://github.com/bids-standard/bids-specification/pull/653) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] Rewrite the MRI/fieldmaps subsection for consistency with the rest of specs [#651](https://github.com/bids-standard/bids-specification/pull/651) ([oesteban](https://github.com/oesteban))
-   \[FIX] Fixing template string on electrodes for eeg and ieeg. [#650](https://github.com/bids-standard/bids-specification/pull/650) ([adam2392](https://github.com/adam2392))
-   ENH: Update genetics-BIDS citation [#646](https://github.com/bids-standard/bids-specification/pull/646) ([effigies](https://github.com/effigies))
-   \[SCHEMA] Add derivatives entities to the schema [#645](https://github.com/bids-standard/bids-specification/pull/645) ([tsalo](https://github.com/tsalo))
-   \[MISC] add brief note that TSV example in the spec may currently use either tab or space characters [#643](https://github.com/bids-standard/bids-specification/pull/643) ([yarikoptic](https://github.com/yarikoptic))
-   \[ENH] Add "multipart DWI" acquisitions and refactor DWI specifications [#624](https://github.com/bids-standard/bids-specification/pull/624) ([oesteban](https://github.com/oesteban))
-   \[SCHEMA] Render schema elements in text [#610](https://github.com/bids-standard/bids-specification/pull/610) ([tsalo](https://github.com/tsalo))
-   \[ENH] Add part entity for complex-valued data [#424](https://github.com/bids-standard/bids-specification/pull/424) ([tsalo](https://github.com/tsalo))

## [v1.4.1](https://github.com/bids-standard/bids-specification/tree/v1.4.1) (2020-10-13)

-   \[INFRA] minor robustness enhancements to pdf build shell script  [#642](https://github.com/bids-standard/bids-specification/pull/642) ([yarikoptic](https://github.com/yarikoptic))
-   \[FIX] consistent CoordinateSystem fields for ephys [#641](https://github.com/bids-standard/bids-specification/pull/641) ([sappelhoff](https://github.com/sappelhoff))
-   REL: v1.4.1 [#640](https://github.com/bids-standard/bids-specification/pull/640) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[INFRA] set up github action to detect latin phrases [#636](https://github.com/bids-standard/bids-specification/pull/636) ([Remi-Gau](https://github.com/Remi-Gau))
-   \[ENH] Add a definition for "deprecation" [#634](https://github.com/bids-standard/bids-specification/pull/634) ([sappelhoff](https://github.com/sappelhoff))
-   \[MISC] consolidate BIDS citations in introduction [#630](https://github.com/bids-standard/bids-specification/pull/630) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] URI "definition" and recommendation [#629](https://github.com/bids-standard/bids-specification/pull/629) ([Remi-Gau](https://github.com/Remi-Gau))
-   \[FIX] change remaining latin expressions (etc and i.e.) [#628](https://github.com/bids-standard/bids-specification/pull/628) ([Remi-Gau](https://github.com/Remi-Gau))
-   \[FIX] replace "e.g.," by "for example" [#626](https://github.com/bids-standard/bids-specification/pull/626) ([Remi-Gau](https://github.com/Remi-Gau))
-   \[FIX] arrays of 3D coordinates MUST supply numeric values in x, y, z order [#623](https://github.com/bids-standard/bids-specification/pull/623) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] Accidentally swapped Neuromag/Elekta/MEGIN cross-talk & fine-calibration filename extensions [#621](https://github.com/bids-standard/bids-specification/pull/621) ([hoechenberger](https://github.com/hoechenberger))
-   \[FIX] improve HED documentation [#619](https://github.com/bids-standard/bids-specification/pull/619) ([VisLab](https://github.com/VisLab))
-   \[INFRA] Move MRI section headings up a level [#618](https://github.com/bids-standard/bids-specification/pull/618) ([tsalo](https://github.com/tsalo))
-   \[INFRA] SCHEMA: Declare entities by concept names, add entity field for filename components [#616](https://github.com/bids-standard/bids-specification/pull/616) ([effigies](https://github.com/effigies))
-   \[FIX] Change wrong text references from \*CoordinateSystemUnits to \*CoordinateUnits [#614](https://github.com/bids-standard/bids-specification/pull/614) ([sappelhoff](https://github.com/sappelhoff))
-   \[ENH] Describe arbitrary units in Common Principles [#606](https://github.com/bids-standard/bids-specification/pull/606) ([tsalo](https://github.com/tsalo))
-   \[FIX] Clarify data types and requirement levels for all JSON files [#605](https://github.com/bids-standard/bids-specification/pull/605) ([sappelhoff](https://github.com/sappelhoff))
-   \[INFRA] downgrade github-changelog-generator to 1.14.3 due to issue with 1.15.2 [#600](https://github.com/bids-standard/bids-specification/pull/600) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] tighter rules for sharing MEG cross-talk and fine-calibration .fif files [#598](https://github.com/bids-standard/bids-specification/pull/598) ([sappelhoff](https://github.com/sappelhoff))
-   \[MISC] Add tsalo as a BIDS maintainer [#597](https://github.com/bids-standard/bids-specification/pull/597) ([tsalo](https://github.com/tsalo))
-   \[FIX] clarify definition of events in common principles [#595](https://github.com/bids-standard/bids-specification/pull/595) ([sappelhoff](https://github.com/sappelhoff))
-   \[INFRA] use --release-branch option in github-changelog-generator [#594](https://github.com/bids-standard/bids-specification/pull/594) ([sappelhoff](https://github.com/sappelhoff))
-   \[ENH] Define "modality" and clarify "data type" [#592](https://github.com/bids-standard/bids-specification/pull/592) ([effigies](https://github.com/effigies))
-   \[FIX] Adjust index definition to be nonnegative integer [#590](https://github.com/bids-standard/bids-specification/pull/590) ([nicholst](https://github.com/nicholst))
-   \[MISC] fix links, make json object links consistent, fix pandoc rendering [#587](https://github.com/bids-standard/bids-specification/pull/587) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] Fix link in Common principles [#583](https://github.com/bids-standard/bids-specification/pull/583) ([tsalo](https://github.com/tsalo))
-   \[ENH] Specify how to share cross-talk and fine-calibration for Neuromag/Elekta/MEGIN data [#581](https://github.com/bids-standard/bids-specification/pull/581) ([sappelhoff](https://github.com/sappelhoff))
-   \[ENH] Specify echo and run indices are nonnegative integers in schema [#578](https://github.com/bids-standard/bids-specification/pull/578) ([tsalo](https://github.com/tsalo))
-   \[ENH] add optional presentation software name, version, OS, and code to events.json [#573](https://github.com/bids-standard/bids-specification/pull/573) ([Remi-Gau](https://github.com/Remi-Gau))
-   \[ENH] added PPG as an accepted channel type for EEG, MEG and iEEG [#570](https://github.com/bids-standard/bids-specification/pull/570) ([robertoostenveld](https://github.com/robertoostenveld))
-   \[INFRA] Move entity definitions to a separate page [#568](https://github.com/bids-standard/bids-specification/pull/568) ([tsalo](https://github.com/tsalo))
-   \[INFRA] enable pandoc emojis for the pdf build [#562](https://github.com/bids-standard/bids-specification/pull/562) ([sappelhoff](https://github.com/sappelhoff))
-   \[INFRA] Auto adjust table fences before PDF conversion [#560](https://github.com/bids-standard/bids-specification/pull/560) ([sebastientourbier](https://github.com/sebastientourbier))
-   \[ENH] Support run and acq entities in behavior-only data [#556](https://github.com/bids-standard/bids-specification/pull/556) ([tsalo](https://github.com/tsalo))
-   \[FIX] Clarify requirement levels for TSV metadata fields [#555](https://github.com/bids-standard/bids-specification/pull/555) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] Reorganize rec, ce entities, \_defacemask [#550](https://github.com/bids-standard/bids-specification/pull/550) ([emdupre](https://github.com/emdupre))
-   \[FIX] Clarify Upper-casing of Channels.tsv Channel Type [#548](https://github.com/bids-standard/bids-specification/pull/548) ([adam2392](https://github.com/adam2392))
-   \[ENH] Extend date time information to include optional UTC syntax, warn about FIF requirements [#546](https://github.com/bids-standard/bids-specification/pull/546) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] clarify that \<physio|stim>.json is REQUIRED [#542](https://github.com/bids-standard/bids-specification/pull/542) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] Replace all non-breaking spaces with vanilla spaces [#536](https://github.com/bids-standard/bids-specification/pull/536) ([nicholst](https://github.com/nicholst))
-   \[FIX] Clarify indices are nonnegative integers. [#535](https://github.com/bids-standard/bids-specification/pull/535) ([nicholst](https://github.com/nicholst))
-   \[FIX] Clarify use of session entity in file names [#532](https://github.com/bids-standard/bids-specification/pull/532) ([Moo-Marc](https://github.com/Moo-Marc))
-   \[ENH] Add the ability of users to specify an explicit HED.xml schema for validation. [#527](https://github.com/bids-standard/bids-specification/pull/527) ([VisLab](https://github.com/VisLab))
-   \[FIX] clarify that scans.json is allowed and recommended [#523](https://github.com/bids-standard/bids-specification/pull/523) ([sappelhoff](https://github.com/sappelhoff))
-   \[INFRA] add copyright holder to license.  [#521](https://github.com/bids-standard/bids-specification/pull/521) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] clarify XXXCoord\* in the coordinate systems appendix [#520](https://github.com/bids-standard/bids-specification/pull/520) ([sappelhoff](https://github.com/sappelhoff))
-   \[ENH] Update `beh/` specification to contrast with any neural recordings [#515](https://github.com/bids-standard/bids-specification/pull/515) ([effigies](https://github.com/effigies))
-   \[Fix] 'segmentation' spelling in 05-derivatives/03-imaging.md [#514](https://github.com/bids-standard/bids-specification/pull/514) ([rwblair](https://github.com/rwblair))
-   \[FIX] restructure and clarify \*\_physio/\*\_stim section [#513](https://github.com/bids-standard/bids-specification/pull/513) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] clarify file formats in EEG, iEEG [#511](https://github.com/bids-standard/bids-specification/pull/511) ([sappelhoff](https://github.com/sappelhoff))
-   \[Fix] Add links and release dates to pre GH changelog, fix formatting [#509](https://github.com/bids-standard/bids-specification/pull/509) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] Clarify that `acq\_time` in `scans.json` refers to first data point acquired [#506](https://github.com/bids-standard/bids-specification/pull/506) ([tsalo](https://github.com/tsalo))
-   \[INFRA] make circle artifact link a GH action, point to pdf [#505](https://github.com/bids-standard/bids-specification/pull/505) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] Typos in DECISION-MAKING file [#504](https://github.com/bids-standard/bids-specification/pull/504) ([tsalo](https://github.com/tsalo))
-   \[ENH] Add `Commenting on a PR` to CONTRIBUTING.md [#490](https://github.com/bids-standard/bids-specification/pull/490) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[FIX] clarify MEG empty-room recording naming conventions [#480](https://github.com/bids-standard/bids-specification/pull/480) ([sappelhoff](https://github.com/sappelhoff))
-   \[INFRA] Convert entity table to yaml [#475](https://github.com/bids-standard/bids-specification/pull/475) ([tsalo](https://github.com/tsalo))
-   \[FIX] Recommend SI units formatting to adhere to CMIXF-12 [#411](https://github.com/bids-standard/bids-specification/pull/411) ([sappelhoff](https://github.com/sappelhoff))

## [v1.4.0](https://github.com/bids-standard/bids-specification/tree/v1.4.0) (2020-06-11)

-   REL: v1.4.0 [#496](https://github.com/bids-standard/bids-specification/pull/496) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[FIX] Clarify language on unsetting a key/value pair [#495](https://github.com/bids-standard/bids-specification/pull/495) ([nicholst](https://github.com/nicholst))
-   \[ENH] optionally allow LICENSE file [#483](https://github.com/bids-standard/bids-specification/pull/483) ([sappelhoff](https://github.com/sappelhoff))
-   \[INFRA] linkchecker - ignore github pull and tree URLs [#477](https://github.com/bids-standard/bids-specification/pull/477) ([yarikoptic](https://github.com/yarikoptic))
-   \[ENH] Allow fractional seconds in scans file datetimes [#470](https://github.com/bids-standard/bids-specification/pull/470) ([tsalo](https://github.com/tsalo))
-   \[MISC] Maintainers - `Scope` responsibility [#467](https://github.com/bids-standard/bids-specification/pull/467) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[FIX] Align tables in MRI section [#465](https://github.com/bids-standard/bids-specification/pull/465) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] Drop `\_part-` reference from example, introduce `\_split-` entity [#460](https://github.com/bids-standard/bids-specification/pull/460) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] clarify participants tsv+json with examples and recommendations [#459](https://github.com/bids-standard/bids-specification/pull/459) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] Remove BESA from list of restricted keywords of EEG coordsystems [#457](https://github.com/bids-standard/bids-specification/pull/457) ([sappelhoff](https://github.com/sappelhoff))
-   \[INFRA] add steps for release protocol (PDF upload) [#455](https://github.com/bids-standard/bids-specification/pull/455) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] Add reference to PDF on front page of specification [#452](https://github.com/bids-standard/bids-specification/pull/452) ([nicholst](https://github.com/nicholst))
-   \[INFRA] Add conditional for link-checking releases [#451](https://github.com/bids-standard/bids-specification/pull/451) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[FIX] unordered list formatting in BEP018 [#449](https://github.com/bids-standard/bids-specification/pull/449) ([sappelhoff](https://github.com/sappelhoff))
-   REL: 1.3.1-dev [#448](https://github.com/bids-standard/bids-specification/pull/448) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[FIX] fix inconsistencies for task label between sections [#446](https://github.com/bids-standard/bids-specification/pull/446) ([Remi-Gau](https://github.com/Remi-Gau))
-   \[FIX] update DECISION-MAKING.md document with new governance [#441](https://github.com/bids-standard/bids-specification/pull/441) ([sappelhoff](https://github.com/sappelhoff))
-   \[ENH] BEP 003: Common Derivatives [#265](https://github.com/bids-standard/bids-specification/pull/265) ([effigies](https://github.com/effigies))
-   \[ENH] Add Glossary of terms/abbreviations used in the specification [#152](https://github.com/bids-standard/bids-specification/pull/152) ([yarikoptic](https://github.com/yarikoptic))

## [v1.3.0](https://github.com/bids-standard/bids-specification/tree/v1.3.0) (2020-04-14)

-   \[INFRA] add zenodo badge to README [#447](https://github.com/bids-standard/bids-specification/pull/447) ([sappelhoff](https://github.com/sappelhoff))
-   \[MISC] Added contributors from VisLab [#444](https://github.com/bids-standard/bids-specification/pull/444) ([VisLab](https://github.com/VisLab))
-   \[FIX] Clarify  snake_case+CamelCase in TSV+JSON [#442](https://github.com/bids-standard/bids-specification/pull/442) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] Eliminate web/online-specific language [#437](https://github.com/bids-standard/bids-specification/pull/437) ([nicholst](https://github.com/nicholst))
-   \[INFRA] ensure build_docs_pdf CircleCI job runs last [#436](https://github.com/bids-standard/bids-specification/pull/436) ([sappelhoff](https://github.com/sappelhoff))
-   REL: v1.3.0 [#435](https://github.com/bids-standard/bids-specification/pull/435) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[INFRA] Add issue templates for GitHub [#434](https://github.com/bids-standard/bids-specification/pull/434) ([sappelhoff](https://github.com/sappelhoff))
-   \[INFRA] Get latest PDF build from CircleCI artifacts [#433](https://github.com/bids-standard/bids-specification/pull/433) ([sappelhoff](https://github.com/sappelhoff))
-   \[INFRA] Update release protocol [#432](https://github.com/bids-standard/bids-specification/pull/432) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[INFRA] add support for building PDF versions of the spec [#431](https://github.com/bids-standard/bids-specification/pull/431) ([Arshitha](https://github.com/Arshitha))
-   \[ENH] Explicitly mention bids-validator and update link [#428](https://github.com/bids-standard/bids-specification/pull/428) ([sappelhoff](https://github.com/sappelhoff))
-   \[INFRA] use new bids-maintenance GitHub account to take over automatic work [#426](https://github.com/bids-standard/bids-specification/pull/426) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] Unify section titles and table-of-contents entries [#422](https://github.com/bids-standard/bids-specification/pull/422) ([nicholst](https://github.com/nicholst))
-   \[INFRA] add # before heading in CHANGES [#419](https://github.com/bids-standard/bids-specification/pull/419) ([sappelhoff](https://github.com/sappelhoff))
-   \[INFRA] fix heading of auto changelog to be a markdown header [#417](https://github.com/bids-standard/bids-specification/pull/417) ([sappelhoff](https://github.com/sappelhoff))
-   REL: 1.3.0-dev [#413](https://github.com/bids-standard/bids-specification/pull/413) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[ENH] Add OPTIONAL EthicsApprovals field to dataset description [#412](https://github.com/bids-standard/bids-specification/pull/412) ([effigies](https://github.com/effigies))
-   \[ENH] BEP 018 - Genetic Information [#395](https://github.com/bids-standard/bids-specification/pull/395) ([effigies](https://github.com/effigies))

## [v1.2.2](https://github.com/bids-standard/bids-specification/tree/v1.2.2) (2020-02-12)

-   \[FIX] improve wording on data dictionaries [#410](https://github.com/bids-standard/bids-specification/pull/410) ([sappelhoff](https://github.com/sappelhoff))
-   \[MISC] update contributions by CPernet [#409](https://github.com/bids-standard/bids-specification/pull/409) ([CPernet](https://github.com/CPernet))
-   REL: v1.2.2 [#405](https://github.com/bids-standard/bids-specification/pull/405) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[MISC] Add Sébastien Tourbier to contributors [#394](https://github.com/bids-standard/bids-specification/pull/394) ([sebastientourbier](https://github.com/sebastientourbier))
-   \[FIX] consistent units description between EEG/MEG/iEEG. Clarify (derived) SI units + prefixes [#391](https://github.com/bids-standard/bids-specification/pull/391) ([sappelhoff](https://github.com/sappelhoff))
-   \[MISC] moved list of extension proposals to the main BIDS website [#389](https://github.com/bids-standard/bids-specification/pull/389) ([robertoostenveld](https://github.com/robertoostenveld))
-   \[FIX] Typos and clarifications [#386](https://github.com/bids-standard/bids-specification/pull/386) ([apjanke](https://github.com/apjanke))
-   \[INFRA] Add watermark to drafts [#383](https://github.com/bids-standard/bids-specification/pull/383) ([effigies](https://github.com/effigies))
-   \[MISC] Teon Brooks retiring moderator duties for BEP021 [#381](https://github.com/bids-standard/bids-specification/pull/381) ([teonbrooks](https://github.com/teonbrooks))
-   \[FIX] clarify that string is expected for HowToAcknowledge field in dataset_description.json [#380](https://github.com/bids-standard/bids-specification/pull/380) ([sappelhoff](https://github.com/sappelhoff))
-   \[MISC] Typo and style [#378](https://github.com/bids-standard/bids-specification/pull/378) ([TheChymera](https://github.com/TheChymera))
-   \[FIX] divide readme into 3 parts [#374](https://github.com/bids-standard/bids-specification/pull/374) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] Refer to BIDS consistently, instead of "\<Modality>-BIDS" [#366](https://github.com/bids-standard/bids-specification/pull/366) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] Change recommended anonymization date from 1900 to 1925 [#363](https://github.com/bids-standard/bids-specification/pull/363) ([alexrockhill](https://github.com/alexrockhill))
-   \[FIX] Minor fixups of inconsistencies while going through a PDF version [#362](https://github.com/bids-standard/bids-specification/pull/362) ([yarikoptic](https://github.com/yarikoptic))
-   \[FIX] clarify that filters should be specified as object of objects [#348](https://github.com/bids-standard/bids-specification/pull/348) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] Clarify channels.tsv is RECOMMENDED consistently across ephys [#347](https://github.com/bids-standard/bids-specification/pull/347) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] Typo fix (contract -> contrast) in events documentation [#346](https://github.com/bids-standard/bids-specification/pull/346) ([snastase](https://github.com/snastase))
-   \[MISC] rm TOC.md - seems no longer pertinent/used [#341](https://github.com/bids-standard/bids-specification/pull/341) ([yarikoptic](https://github.com/yarikoptic))
-   \[MISC] Move the PR template to a separate folder and improve contents [#338](https://github.com/bids-standard/bids-specification/pull/338) ([jhlegarreta](https://github.com/jhlegarreta))
-   \[INFRA] Find npm requirements file in Circle [#336](https://github.com/bids-standard/bids-specification/pull/336) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[ENH] Clarify phenotypic and assessment data in new section [#331](https://github.com/bids-standard/bids-specification/pull/331) ([sappelhoff](https://github.com/sappelhoff))
-   \[MISC] add information about continuous integration checks to PR template [#330](https://github.com/bids-standard/bids-specification/pull/330) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] Fix `Common principles` `Key/value files` section level [#328](https://github.com/bids-standard/bids-specification/pull/328) ([jhlegarreta](https://github.com/jhlegarreta))
-   \[INFRA] Set the maximum heading length lint check to `false` [#325](https://github.com/bids-standard/bids-specification/pull/325) ([jhlegarreta](https://github.com/jhlegarreta))
-   \[FIX] Number explicitly all cases in MRI field map section headers [#323](https://github.com/bids-standard/bids-specification/pull/323) ([jhlegarreta](https://github.com/jhlegarreta))
-   \[FIX] Add SoftwareFilters to EEG sidecar example [#322](https://github.com/bids-standard/bids-specification/pull/322) ([Remi-Gau](https://github.com/Remi-Gau))
-   \[MISC] Fixing Travis errors with Remark [#320](https://github.com/bids-standard/bids-specification/pull/320) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[INFRA] Link to doc builds in CI checks [#315](https://github.com/bids-standard/bids-specification/pull/315) ([jasmainak](https://github.com/jasmainak))
-   \[MISC] Add BEP027 - BIDS Execution to BEP list [#314](https://github.com/bids-standard/bids-specification/pull/314) ([effigies](https://github.com/effigies))
-   \[FIX] Add CBV and phase to Entity table [#312](https://github.com/bids-standard/bids-specification/pull/312) ([tsalo](https://github.com/tsalo))
-   \[FIX] Normalization of template-generated standard spaces [#306](https://github.com/bids-standard/bids-specification/pull/306) ([oesteban](https://github.com/oesteban))
-   \[ENH] Release protocol notes [#304](https://github.com/bids-standard/bids-specification/pull/304) ([franklin-feingold](https://github.com/franklin-feingold))
-   REL: 1.3.0-dev [#303](https://github.com/bids-standard/bids-specification/pull/303) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[INFRA] Adding contributor appendix sentence to PR template  [#299](https://github.com/bids-standard/bids-specification/pull/299) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[ENH] Added discontinuous datatype for EEG and iEEG [#286](https://github.com/bids-standard/bids-specification/pull/286) ([wouterpotters](https://github.com/wouterpotters))
-   \[FIX] Clarify paragraph about custom data types [#264](https://github.com/bids-standard/bids-specification/pull/264) ([effigies](https://github.com/effigies))

## [v1.2.1](https://github.com/bids-standard/bids-specification/tree/v1.2.1) (2019-08-14)

-   FIX: repair link in anatomical MRI table [#297](https://github.com/bids-standard/bids-specification/pull/297) ([sappelhoff](https://github.com/sappelhoff))
-   \[ENH] Clarify requirements in Release Protocol [#294](https://github.com/bids-standard/bids-specification/pull/294) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[INFRA+FIX] Use linkchecker (from a dedicated docker image) to check all URLs [#293](https://github.com/bids-standard/bids-specification/pull/293) ([yarikoptic](https://github.com/yarikoptic))
-   REL: v1.2.1 [#291](https://github.com/bids-standard/bids-specification/pull/291) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[ENH] Adding Contributors and updating contributions [#284](https://github.com/bids-standard/bids-specification/pull/284) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[MISC] update Code of Conduct contact [#281](https://github.com/bids-standard/bids-specification/pull/281) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[ENH] Update contributing guide and README to make discussion forums easy to find [#279](https://github.com/bids-standard/bids-specification/pull/279) ([emdupre](https://github.com/emdupre))
-   \[ENH] Starter Kit dropdown menu [#278](https://github.com/bids-standard/bids-specification/pull/278) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[ENH] BEP Update [#277](https://github.com/bids-standard/bids-specification/pull/277) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[INFRA] Update pipenv [#274](https://github.com/bids-standard/bids-specification/pull/274) ([sappelhoff](https://github.com/sappelhoff))
-   \[INFRA] Transpose the entity table and link to text anchors describing each entity [#272](https://github.com/bids-standard/bids-specification/pull/272) ([sappelhoff](https://github.com/sappelhoff))
-   \[ENH] Add Twitter badge to README and link to website to landing page [#268](https://github.com/bids-standard/bids-specification/pull/268) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[ENH] adding release guidelines [#267](https://github.com/bids-standard/bids-specification/pull/267) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[FIX] Common principles: Fix filename in inheritance principle [#261](https://github.com/bids-standard/bids-specification/pull/261) ([Lestropie](https://github.com/Lestropie))
-   \[MISC] update modality references [#258](https://github.com/bids-standard/bids-specification/pull/258) ([sappelhoff](https://github.com/sappelhoff))
-   \[INFRA] adding logo to RTD [#256](https://github.com/bids-standard/bids-specification/pull/256) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[INFRA] add footer, replacing mkdocs/material advert with Github link [#250](https://github.com/bids-standard/bids-specification/pull/250) ([sappelhoff](https://github.com/sappelhoff))
-   \[MISC] rename logo files, add a README of where they come from, fix favicon [#249](https://github.com/bids-standard/bids-specification/pull/249) ([sappelhoff](https://github.com/sappelhoff))
-   \[MISC] updating MEG doc links, manufacturer names, and adding a missing MEG example [#248](https://github.com/bids-standard/bids-specification/pull/248) ([sappelhoff](https://github.com/sappelhoff))
-   \[ENH] Add favicon to RTD [#246](https://github.com/bids-standard/bids-specification/pull/246) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[MISC] Update Authors in BEP025 [#241](https://github.com/bids-standard/bids-specification/pull/241) ([josator2](https://github.com/josator2))
-   \[MISC] Document BEPs that are not active anymore, but have not been merged [#240](https://github.com/bids-standard/bids-specification/pull/240) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] remove ManufacturersAmplifierModelName (again) [#236](https://github.com/bids-standard/bids-specification/pull/236) ([robertoostenveld](https://github.com/robertoostenveld))
-   \[INFRA] Update release protocol [#235](https://github.com/bids-standard/bids-specification/pull/235) ([effigies](https://github.com/effigies))
-   REL: 1.3.0-dev [#234](https://github.com/bids-standard/bids-specification/pull/234) ([effigies](https://github.com/effigies))
-   \[INFRA] Enable version panel for quickly finding previous versions [#232](https://github.com/bids-standard/bids-specification/pull/232) ([effigies](https://github.com/effigies))
-   \[FIX] Clarify Appendix II: The list of licenses only lists examples [#222](https://github.com/bids-standard/bids-specification/pull/222) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] Trivial column header fix  [#220](https://github.com/bids-standard/bids-specification/pull/220) ([nicholst](https://github.com/nicholst))
-   \[INFRA] Add clarification on merge methods to DECISION_MAKING [#217](https://github.com/bids-standard/bids-specification/pull/217) ([sappelhoff](https://github.com/sappelhoff))
-   \[INFRA] Enable permalink urls to appear at (sub)section headings [#214](https://github.com/bids-standard/bids-specification/pull/214) ([yarikoptic](https://github.com/yarikoptic))
-   \[INFRA] bump up mkdocs-materials version [#211](https://github.com/bids-standard/bids-specification/pull/211) ([sappelhoff](https://github.com/sappelhoff))
-   \[MISC] Fix github username for @chrisgorgo [#204](https://github.com/bids-standard/bids-specification/pull/204) ([chrisgorgo](https://github.com/chrisgorgo))
-   \[FIX] clarify example 3  in common principles (inheritance) [#202](https://github.com/bids-standard/bids-specification/pull/202) ([sappelhoff](https://github.com/sappelhoff))
-   \[MISC] Expand entity table for MEG/EEG/iEEG specific files [#198](https://github.com/bids-standard/bids-specification/pull/198) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] make iEEG ToC more consistent with MEG and EEG [#191](https://github.com/bids-standard/bids-specification/pull/191) ([robertoostenveld](https://github.com/robertoostenveld))
-   \[FIX] Clarify use of acq and task parameters in EEG, MEG, and iEEG [#188](https://github.com/bids-standard/bids-specification/pull/188) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] clarify use of tools for CTF data renaming [#187](https://github.com/bids-standard/bids-specification/pull/187) ([sappelhoff](https://github.com/sappelhoff))
-   \[MISC] Add bep006 and bep010 to completed beps and fix links [#186](https://github.com/bids-standard/bids-specification/pull/186) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] change file for definition of electrical stimulation labels from \_electrodes.json to \_events.json [#185](https://github.com/bids-standard/bids-specification/pull/185) ([ezemikulan](https://github.com/ezemikulan))
-   \[ENH] relax ieeg channel name requirements of letters and numbers only [#182](https://github.com/bids-standard/bids-specification/pull/182) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] make MEG section headings and ToC consistent to the EEG and iEEG specs [#181](https://github.com/bids-standard/bids-specification/pull/181) ([robertoostenveld](https://github.com/robertoostenveld))
-   \[FIX] make section headings and ToC consistent between meg and eeg specs [#180](https://github.com/bids-standard/bids-specification/pull/180) ([robertoostenveld](https://github.com/robertoostenveld))
-   \[MISC] Spelling fixes [#179](https://github.com/bids-standard/bids-specification/pull/179) ([DimitriPapadopoulos](https://github.com/DimitriPapadopoulos))
-   \[ENH] Alternative folder organization for raw, derived, and source data [#178](https://github.com/bids-standard/bids-specification/pull/178) ([chrisgorgo](https://github.com/chrisgorgo))
-   \[INFRA] Adding instructions for naming PRs [#177](https://github.com/bids-standard/bids-specification/pull/177) ([chrisgorgo](https://github.com/chrisgorgo))
-   \[MISC] Introducing Stefan Appelhoff as the first Maintainer [#176](https://github.com/bids-standard/bids-specification/pull/176) ([chrisgorgo](https://github.com/chrisgorgo))
-   \[FIX] Clarify name of "BrainVision" format [#175](https://github.com/bids-standard/bids-specification/pull/175) ([JegouA](https://github.com/JegouA))
-   \[FIX] Fixes spelling of continuous [#171](https://github.com/bids-standard/bids-specification/pull/171) ([emdupre](https://github.com/emdupre))
-   \[FIX] Clarify continuous recording metadata fields [#167](https://github.com/bids-standard/bids-specification/pull/167) ([effigies](https://github.com/effigies))
-   \[FIX] changed reference of `dcm2nii` to `dcm2niix` [#166](https://github.com/bids-standard/bids-specification/pull/166) ([DimitriPapadopoulos](https://github.com/DimitriPapadopoulos))
-   \[FIX] Removing a leftover file [#162](https://github.com/bids-standard/bids-specification/pull/162) ([chrisgorgo](https://github.com/chrisgorgo))
-   \[FIX] Specify marker file names for KIT data (MEG) [#62](https://github.com/bids-standard/bids-specification/pull/62) ([monkeyman192](https://github.com/monkeyman192))
-   \[FIX] Remove father-level for meg filetypes other than BTi/4D data [#19](https://github.com/bids-standard/bids-specification/pull/19) ([teonbrooks](https://github.com/teonbrooks))

## [v1.2.0](https://github.com/bids-standard/bids-specification/tree/v1.2.0) (2019-03-04)

-   REL: v1.2.0 [#161](https://github.com/bids-standard/bids-specification/pull/161) ([chrisgorgo](https://github.com/chrisgorgo))
-   \[MISC] Adding Dimitri Papadopoulos Orfanos to the list of contributors [#157](https://github.com/bids-standard/bids-specification/pull/157) ([DimitriPapadopoulos](https://github.com/DimitriPapadopoulos))
-   \[FIX] use "specification" not "protocol" to refer to BIDS [#156](https://github.com/bids-standard/bids-specification/pull/156) ([yarikoptic](https://github.com/yarikoptic))
-   \[FIX] Fix example misalignment [#155](https://github.com/bids-standard/bids-specification/pull/155) ([DimitriPapadopoulos](https://github.com/DimitriPapadopoulos))
-   \[INFRA] Update Pipfile.lock [#144](https://github.com/bids-standard/bids-specification/pull/144) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[ENH] clarify decimal sep and numerical notation convention [#143](https://github.com/bids-standard/bids-specification/pull/143) ([sappelhoff](https://github.com/sappelhoff))
-   \[ENH] clarify encoding of README, CHANGES, TSV, and JSON files [#140](https://github.com/bids-standard/bids-specification/pull/140) ([sappelhoff](https://github.com/sappelhoff))
-   \[MISC] Update site_name and release protocol [#137](https://github.com/bids-standard/bids-specification/pull/137) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[FIX] Example for IntendedFor was missing session indicator in the filename [#129](https://github.com/bids-standard/bids-specification/pull/129) ([yarikoptic](https://github.com/yarikoptic))
-   \[ENH] Add "\_phase" suffix to func datatype for functional phase data [#128](https://github.com/bids-standard/bids-specification/pull/128) ([tsalo](https://github.com/tsalo))
-   \[MISC] Update to Release_Protocol.md [#126](https://github.com/bids-standard/bids-specification/pull/126) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[MISC] Update tag naming convention [#123](https://github.com/bids-standard/bids-specification/pull/123) ([chrisgorgo](https://github.com/chrisgorgo))
-   \[ENH] Merge bep006 and bep010 [#108](https://github.com/bids-standard/bids-specification/pull/108) ([sappelhoff](https://github.com/sappelhoff))
-   \[MISC] Adding formal decision-making rules [#104](https://github.com/bids-standard/bids-specification/pull/104) ([chrisgorgo](https://github.com/chrisgorgo))
-   \[FIX] number of small corrections to the specification [#98](https://github.com/bids-standard/bids-specification/pull/98) ([robertoostenveld](https://github.com/robertoostenveld))

## [v1.1.2](https://github.com/bids-standard/bids-specification/tree/v1.1.2) (2019-01-10)

-   REL: v.1.1.2 [#121](https://github.com/bids-standard/bids-specification/pull/121) ([chrisgorgo](https://github.com/chrisgorgo))
-   \[MISC] Update 01-contributors.md [#120](https://github.com/bids-standard/bids-specification/pull/120) ([oesteban](https://github.com/oesteban))
-   \[ENH] Global fields in data dictionaries [#117](https://github.com/bids-standard/bids-specification/pull/117) ([chrisgorgo](https://github.com/chrisgorgo))
-   \[MISC] Propose BEP026 MER [#116](https://github.com/bids-standard/bids-specification/pull/116) ([greydongilmore](https://github.com/greydongilmore))
-   \[FIX] Remove duplicate entries in MEG table [#113](https://github.com/bids-standard/bids-specification/pull/113) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[MISC] Propose BEP025 MIDS [#110](https://github.com/bids-standard/bids-specification/pull/110) ([josator2](https://github.com/josator2))
-   FIX] repair links [#106](https://github.com/bids-standard/bids-specification/pull/106) ([sappelhoff](https://github.com/sappelhoff))
-   \[INFRA] Autogenerate CHANGES.md [#103](https://github.com/bids-standard/bids-specification/pull/103) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[MISC] Added contributor information [#100](https://github.com/bids-standard/bids-specification/pull/100) ([jgrethe](https://github.com/jgrethe))
-   \[ENH] First(?) good practice recommendation. No excessive overrides in Inheritance principle [#99](https://github.com/bids-standard/bids-specification/pull/99) ([yarikoptic](https://github.com/yarikoptic))
-   \[MISC] adding extensions page [#97](https://github.com/bids-standard/bids-specification/pull/97) ([choldgraf](https://github.com/choldgraf))
-   \[FIX] fix some urls (as detected to be broken/inconsistent) [#95](https://github.com/bids-standard/bids-specification/pull/95) ([yarikoptic](https://github.com/yarikoptic))
-   \[MISC] Change BEP numbers to include MRS [#94](https://github.com/bids-standard/bids-specification/pull/94) ([Hboni](https://github.com/Hboni))
-   \[FIX] harmonize and thus shorten templates etc [#93](https://github.com/bids-standard/bids-specification/pull/93) ([yarikoptic](https://github.com/yarikoptic))
-   \[MISC] put links and some text into README [#91](https://github.com/bids-standard/bids-specification/pull/91) ([sappelhoff](https://github.com/sappelhoff))
-   \[MISC] Add extension proposal in 01-introduction.md [#88](https://github.com/bids-standard/bids-specification/pull/88) ([Hboni](https://github.com/Hboni))
-   \[FIX] additional table to recap 'volume acquisition timing' [#87](https://github.com/bids-standard/bids-specification/pull/87) ([Remi-Gau](https://github.com/Remi-Gau))
-   \[FIX] Small typo in "scanning sequence" DICOM tag [#84](https://github.com/bids-standard/bids-specification/pull/84) ([Remi-Gau](https://github.com/Remi-Gau))
-   \[MISC] Update 01-contributors.md [#83](https://github.com/bids-standard/bids-specification/pull/83) ([teonbrooks](https://github.com/teonbrooks))
-   \[ENH] Added CBV contrast [#82](https://github.com/bids-standard/bids-specification/pull/82) ([TheChymera](https://github.com/TheChymera))
-   \[MISC] Add CC-BY 4.0 license [#81](https://github.com/bids-standard/bids-specification/pull/81) ([KirstieJane](https://github.com/KirstieJane))
-   \[INFRA] Fix Travis break [#80](https://github.com/bids-standard/bids-specification/pull/80) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[ENH] allow \_dir for other EPI (func, dwi) sequences [#78](https://github.com/bids-standard/bids-specification/pull/78) ([yarikoptic](https://github.com/yarikoptic))
-   \[MISC] Added appendix to mkdocs and added some internal links [#77](https://github.com/bids-standard/bids-specification/pull/77) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[MISC] added JC Houde as contributor. [#76](https://github.com/bids-standard/bids-specification/pull/76) ([jchoude](https://github.com/jchoude))
-   \[MISC] Updated my contributions [#75](https://github.com/bids-standard/bids-specification/pull/75) ([nicholst](https://github.com/nicholst))
-   \[FIX] update HED appendix [#74](https://github.com/bids-standard/bids-specification/pull/74) ([sappelhoff](https://github.com/sappelhoff))
-   \[FIX] unicode: replace greek mu and omega by micro and ohm signs [#73](https://github.com/bids-standard/bids-specification/pull/73) ([sappelhoff](https://github.com/sappelhoff))
-   \[MISC] Update 01-contributors.md [#72](https://github.com/bids-standard/bids-specification/pull/72) ([francopestilli](https://github.com/francopestilli))
-   \[ENH] add ce-\<label> for fmri data [#70](https://github.com/bids-standard/bids-specification/pull/70) ([dasturge](https://github.com/dasturge))
-   \[INFRA] pin pip version [#68](https://github.com/bids-standard/bids-specification/pull/68) ([chrisgorgo](https://github.com/chrisgorgo))
-   \[MISC] Fix link in index [#46](https://github.com/bids-standard/bids-specification/pull/46) ([chrisgorgo](https://github.com/chrisgorgo))
-   \[MISC] edit contributing guide [#44](https://github.com/bids-standard/bids-specification/pull/44) ([Park-Patrick](https://github.com/Park-Patrick))
-   \[INFRA] Mkdocs configuration and RTD setup [#42](https://github.com/bids-standard/bids-specification/pull/42) ([choldgraf](https://github.com/choldgraf))
-   \[MISC] Move definitions, compulsory, and raw/derivatives sections to principles [#40](https://github.com/bids-standard/bids-specification/pull/40) ([chrisgorgo](https://github.com/chrisgorgo))
-   \[MISC] Remove duplicate section [#39](https://github.com/bids-standard/bids-specification/pull/39) ([chrisgorgo](https://github.com/chrisgorgo))
-   \[INFRA] mkdocs rendering [#36](https://github.com/bids-standard/bids-specification/pull/36) ([chrisgorgo](https://github.com/chrisgorgo))
-   \[MISC] Style consistency [#35](https://github.com/bids-standard/bids-specification/pull/35) ([chrisgorgo](https://github.com/chrisgorgo))
-   \[MISC] Renaming files to conform with style guide [#34](https://github.com/bids-standard/bids-specification/pull/34) ([chrisgorgo](https://github.com/chrisgorgo))
-   \[INFRA] enable travis cache [#32](https://github.com/bids-standard/bids-specification/pull/32) ([chrisgorgo](https://github.com/chrisgorgo))
-   \[MISC] corrected link that is shown for CC0 [#31](https://github.com/bids-standard/bids-specification/pull/31) ([robertoostenveld](https://github.com/robertoostenveld))
-   \[INFRA] added linter integration via travis [#30](https://github.com/bids-standard/bids-specification/pull/30) ([chrisgorgo](https://github.com/chrisgorgo))
-   \[MISC] Cleanup [#29](https://github.com/bids-standard/bids-specification/pull/29) ([chrisgorgo](https://github.com/chrisgorgo))
-   \[MISC] split intro, commons, mr, and meg into folder from specification.md [#28](https://github.com/bids-standard/bids-specification/pull/28) ([teonbrooks](https://github.com/teonbrooks))
-   \[MISC] Add some bids starter kit contributors [#27](https://github.com/bids-standard/bids-specification/pull/27) ([KirstieJane](https://github.com/KirstieJane))
-   \[MISC] Embedded footnotes into text [#25](https://github.com/bids-standard/bids-specification/pull/25) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[MISC] Making HED Strategy Guide link prettier [#24](https://github.com/bids-standard/bids-specification/pull/24) ([fake-filo](https://github.com/fake-filo))
-   \[MISC] more cleanup [#21](https://github.com/bids-standard/bids-specification/pull/21) ([chrisgorgo](https://github.com/chrisgorgo))
-   \[MISC] formatted MEG (8.4) [#17](https://github.com/bids-standard/bids-specification/pull/17) ([franklin-feingold](https://github.com/franklin-feingold))
-   \[MISC] small fixes [#16](https://github.com/bids-standard/bids-specification/pull/16) ([chrisgorgo](https://github.com/chrisgorgo))
-   \[MISC] Add meg img [#14](https://github.com/bids-standard/bids-specification/pull/14) ([sappelhoff](https://github.com/sappelhoff))
-   \[WIP] Cleaning up the specification [#13](https://github.com/bids-standard/bids-specification/pull/13) ([chrisgorgo](https://github.com/chrisgorgo))
-   \[MISC] Adding code of conduct [#6](https://github.com/bids-standard/bids-specification/pull/6) ([chrisgorgo](https://github.com/chrisgorgo))
-   \[INFRA] Renaming the main document [#1](https://github.com/bids-standard/bids-specification/pull/1) ([chrisgorgo](https://github.com/chrisgorgo))

## [1.1.1](https://doi.org/10.5281/zenodo.3759805) (2018-06-06)

-   Improved the MEG landmark coordinates description.
-   Replaced `ManufacturersCapModelName` in `meg.json` with `CapManufacturer` and `CapManufacturersModelName`.
-   Remove `EEGSamplingFrequency` and `ManufacturersAmplifierModelName` from the `meg.json.`
-   Improved the behavioral data description.

## [1.1.0](https://doi.org/10.5281/zenodo.3759802) (2018-04-19)

-   Added support for MEG data (merged BEP008)
-   Added `SequenceName` field.
-   Added support for describing events with Hierarchical Event Descriptors \[[4.3 Task events](04-modality-specific-files/05-task-events.md)].
-   Added `VolumeTiming` and `AcquisitionDuration` fields \[[4.1 Task (including resting state) imaging data](04-modality-specific-files/01-magnetic-resonance-imaging-data.md#task-including-resting-state-imaging-data)].
-   Added `DwellTime` field.

## [1.0.2](https://doi.org/10.5281/zenodo.3759801) (2017-07-18)

-   Added support for high resolution (anatomical) T2star images \[[4.1 Anatomy imaging data](04-modality-specific-files/01-magnetic-resonance-imaging-data.md#anatomy-imaging-data)].
-   Added support for multiple defacing masks \[[4.1 Anatomy imaging data](04-modality-specific-files/01-magnetic-resonance-imaging-data.md#anatomy-imaging-data)].
-   Added optional key and metadata field for contrast enhanced structural scans \[[4.1 Anatomy imaging data](04-modality-specific-files/01-magnetic-resonance-imaging-data.md#anatomy-imaging-data)]
-   Added `DelayTime` field \[[4.1 Task (including resting state) imaging data](04-modality-specific-files/01-magnetic-resonance-imaging-data.md#task-including-resting-state-imaging-data)].
-   Added support for multi echo BOLD data \[[4.1 Task (including resting state) imaging data](04-modality-specific-files/01-magnetic-resonance-imaging-data.md#task-including-resting-state-imaging-data)].

## [1.0.1](https://doi.org/10.5281/zenodo.3759788) (2017-03-13)

-   Added `InstitutionName` field \[[4.1 Task (including resting state) imaging data](04-modality-specific-files/01-magnetic-resonance-imaging-data.md#task-including-resting-state-imaging-data)].
-   Added `InstitutionAddress` field \[[4.1 Task (including resting state) imaging data](04-modality-specific-files/01-magnetic-resonance-imaging-data.md#task-including-resting-state-imaging-data)].
-   Added `DeviceSerialNumber` field \[[4.1 Task (including resting state) imaging data](04-modality-specific-files/01-magnetic-resonance-imaging-data.md#task-including-resting-state-imaging-data)].
-   Added `NumberOfVolumesDiscardedByUser` and `NumberOfVolumesDiscardedByScanner` field \[[4.1 Task (including resting state) imaging data](04-modality-specific-files/01-magnetic-resonance-imaging-data.md#task-including-resting-state-imaging-data)].
-   Added `TotalReadoutTime to` functional images metadata list \[[4.1 Task (including resting state) imaging data](04-modality-specific-files/01-magnetic-resonance-imaging-data.md#task-including-resting-state-imaging-data)].

## 1.0.1-rc1

-   Added T1 Rho maps \[[4.1 Anatomy imaging data](04-modality-specific-files/01-magnetic-resonance-imaging-data.md#anatomy-imaging-data)].
-   Added support for phenotypic information split into multiple files \[[3.2 Participant key file](03-modality-agnostic-files.md#participants-file)].
-   Added recommendations for multi site datasets
-   Added `SoftwareVersions`
-   Added `run-<run_index>` to the phase encoding maps. Improved the description.
-   Added `InversionTime` metadata key.
-   Clarification on the source vs raw language.
-   Added `trial_type` column to the event files.
-   Added missing `sub-<participant_label>` in behavioral data file names
-   Added ability to store stimuli files.
-   Clarified the language describing allowed subject labels.
-   Added quantitative proton density maps.

## [1.0.0](https://doi.org/10.5281/zenodo.3686062) (2016-06-23)

-   Added ability to specify fieldmaps acquired with multiple parameter sets.
-   Added ability to have multiple runs of the same fieldmap.
-   Added FLASH anatomical images.

## 1.0.0-rc4

-   Replaced links to neurolex with explicit DICOM Tags.
-   Added sourcedata.
-   Added data dictionaries.
-   Be more explicit about contents of JSON files for structural (anatomical) scans.

## 1.0.0-rc3

-   Renamed `PhaseEncodingDirection` values from "x", "y", "z" to "i", "j", "k" to avoid confusion with FSL parameters
-   Renamed `SliceEncodingDirection` values from "x", "y", "z" to "i", "j", "k"

## 1.0.0-rc2

-   Removed the requirement that TSV files cannot include more than two consecutive spaces.
-   Refactor of the definitions sections (copied from the manuscript)
-   Make support for uncompressed `.nii` files more explicit.
-   Added `BIDSVersion` to `dataset.json`
-   Remove the statement that `SliceEncodingDirection` is necessary for slice time correction
-   Change dicom converter recommendation from dcmstack to dcm2nii and dicm2nii following interactions with the community (see <https://github.com/moloney/dcmstack/issues/39> and <https://github.com/neurolabusc/dcm2niix/issues/4>).
-   Added section on behavioral experiments with no accompanying MRI acquisition
-   Add `_magnitude.nii[.gz]` image for GE type fieldmaps.
-   Replaced EchoTimeDifference with EchoTime1 and EchoTime2 (SPM toolbox requires this input).
-   Added support for single band reference image for DWI.
-   Added DatasetDOI field in the dataset description.
-   Added description of more metadata fields relevant to DWI fieldmap correction.
-   PhaseEncodingDirection is now expressed in "x", "y" etc. instead of "PA" "RL" for DWI scans (so it's the same as BOLD scans)
-   Added `rec-<label>` flag to BOLD files to distinguish between different reconstruction algorithms (analogous to anatomical scans).
-   Added recommendation to use `_physio` suffix for continuous recordings of motion parameters obtained by the scanner side reconstruction algorithms.

## 1.0.0-rc1

-   Initial release

\* *This Change Log was automatically generated by [github_changelog_generator](https://github.com/skywinder/Github-Changelog-Generator)*
