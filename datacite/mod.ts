/**
 * DataCite Metadata Schema JSON Schemas
 *
 * The DataCite Metadata Working Group publishes a schema as XSD:
 * https://github.com/datacite/schema/tree/master/source/meta
 *
 * Invenio Software publishes JSON Schema versions:
 * https://github.com/inveniosoftware/datacite/tree/master/datacite/schemas
 *
 * This package re-exports the Invenio Software JSON Schemas for easier consumption.
 * The schemas are licensed under BSD-3-Clause (see ./schemas/LICENSE).
 */
export { default as schema40 } from "./schemas/datacite-v4.0.json" with { type: "json" };
export { default as schema41 } from "./schemas/datacite-v4.1.json" with { type: "json" };
export { default as schema42 } from "./schemas/datacite-v4.2.json" with { type: "json" };
export { default as schema43 } from "./schemas/datacite-v4.3.json" with { type: "json" };
export { default as schema44 } from "./schemas/datacite-v4.4.json" with { type: "json" };
export { default as schema45 } from "./schemas/datacite-v4.5.json" with { type: "json" };

export const latest = schema45;
export const versions = {
  "4": schema45,
  "4.5": schema45,
  "4.4": schema44,
  "4.3": schema43,
  "4.2": schema42,
  "4.1": schema41,
  "4.0": schema40,
};
