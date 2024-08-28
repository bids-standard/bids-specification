import type { Schema } from "./metaschema.ts";
import { default as schemaObject } from "./schema.json" with { type: "json" };

export const schema = schemaObject as unknown as Schema;

export type { Schema } from "./metaschema.ts";
export type { Context } from "./context.ts";
export type ObjectSchema = typeof schema.objects;
export type RulesSchema = typeof schema.rules;
