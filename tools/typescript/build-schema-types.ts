import { parse } from 'https://deno.land/std@0.138.0/encoding/yaml.ts'
import { join } from 'https://deno.land/std@0.138.0/path/mod.ts'
import { createSourceFile, generateTypes, print } from './generate.ts'

const contextPath = join('..', '..', 'src', 'schema', 'meta', 'context.yaml')

async function buildContextTypes() {
  const contextSchema = parse(await Deno.readTextFile(contextPath)) as Record<
    string,
    any
  >
  // Compiler configuration
  const output = createSourceFile('context.ts')

  // Test if the file has a sane root level object definition
  if (
    contextSchema.hasOwnProperty('context') &&
    contextSchema.context.type === 'object'
  ) {
    output.statements = generateTypes(contextSchema)
    console.log(print(output))
  } else {
    throw new Error('Could not find definition for Context type')
  }
}

buildContextTypes()
