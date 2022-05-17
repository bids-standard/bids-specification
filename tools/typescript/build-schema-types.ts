import {
  ts,
  createProject,
} from 'https://deno.land/x/ts_morph@14.0.0/bootstrap/mod.ts'
import { parse } from 'https://deno.land/std@0.138.0/encoding/yaml.ts'
import { join } from 'https://deno.land/std@0.138.0/path/mod.ts'
import { createSourceFile, generateTypes, print } from './generate.ts'

const contextPath = join('src', 'schema', 'meta', 'context.yaml')
const libraryPath = join('tools', 'typescript', 'output')

async function buildContextTypes() {
  const contextSchema = parse(await Deno.readTextFile(contextPath)) as Record<
    string,
    any
  >

  const project = await createProject({
    compilerOptions: {
      outDir: join(libraryPath, 'dist'),
      target: ts.ScriptTarget.ESNext,
      declaration: true,
    },
  })

  // Test if the file has a sane root level object definition
  if (
    contextSchema.hasOwnProperty('context') &&
    contextSchema.context.type === 'object'
  ) {
    // Setup output directory
    await Deno.mkdir(join(libraryPath, 'src'), { recursive: true })
    const contextFilePath = join(libraryPath, 'src', 'context.ts')
    // Get a ts.SourceFile from the compiler initially (to add AST to it)
    const contextFile = createSourceFile(contextFilePath)
    // Generate types and add to the source file object
    contextFile.statements = generateTypes(contextSchema)
    // Use the TypeScript printer to format file as string
    const source = print(contextFile)
    // Write string out to the src tree
    await Deno.writeTextFile(contextFilePath, source)
    // Add source file to our project for type checking
    await project.addSourceFilesByPaths(join(libraryPath, 'src', '**', '*.ts'))
    // Output `dist` dir
    const program = project.createProgram([contextFilePath])
    // Display any compiler diagnostics in case the output is incorrect
    const diagnostics = ts.getPreEmitDiagnostics(program)
    const formattedDiagnostic =
      project.formatDiagnosticsWithColorAndContext(diagnostics)
    if (formattedDiagnostic) {
      console.log(source)
      console.log(formattedDiagnostic)
    }
    await program.emit()
    console.log(`TypeScript package generated at path '${libraryPath}'`)
  } else {
    throw new Error('Could not find definition for Context type')
  }
}

buildContextTypes()
