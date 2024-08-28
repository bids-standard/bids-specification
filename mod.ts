import type { Metaschema } from "./metaschema.ts";
export type { Context } from "./context.ts";
export { default as schemaObject } from "./schema.json" with { type: "json" };

export type Schema = Metaschema;
export const schema = schemaObject as Schema;

export type ObjectSchema = typeof schema.objects;
export type RulesSchema = typeof schema.rules;
