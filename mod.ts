/**
 * BIDS Schema object and types
 *
 * This module exports the BIDS Schema object and types for working with it.
 *
 * ```ts no-eval
 * import type { Schema, Context } from 'jsr:@bids/schema'
 * import { schema } from 'jsr:@bids/schema'
 *
 * const metadataFields = schema.objects.metadata
 * const filenameRules = schema.rules.files
 * ```
 *
 * The `Schema` type is derived from the JSON Schema of the BIDS Schema object.
 * The `Context` type is derived from the `schema.meta.context` object, interpreted
 * as a JSON Schema.
 *
 * Because these files are auto-generated, they have no documentation of their own.
 */
import type { Schema } from "./metaschema.ts";
import { default as schemaObject } from "./schema.json" with { type: "json" };

export const schema = schemaObject as unknown as Schema;

export type { Schema } from "./metaschema.ts";
export type { Context } from "./context.ts";
export type ObjectSchema = typeof schema.objects;
export type RulesSchema = typeof schema.rules;
