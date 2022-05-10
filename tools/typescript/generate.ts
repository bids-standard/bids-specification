/**
 * Use the TypeScript compiler to output type definitions based on yaml schema
 *
 * See https://ts-morph.com/ documentation for compiler usage
 */
import { ts } from 'https://deno.land/x/ts_morph@14.0.0/bootstrap/mod.ts'

function capitalize(str) {
  return `${str.charAt(0).toUpperCase()}${str.slice(1)}`
}

/**
 * Convert schema primitives to nearest JS equivalent
 */
function mapSchemaType(typename) {
  if ('integer') return 'number'
  return typename
}

// Flag for exporting interfaces
const interfaceExport = ts.factory.createModifiersFromModifierFlags(
  ts.ModifierFlags.Export
)

export function generateObjectDefinition(name, definition): Array<ts.Node> {
  const customTypeInterfaces = []
  // Construct all properties of the interface
  const interfaceProps = Object.entries(definition.properties).map(
    ([key, value]) => {
      // Test for an nested interface we can define
      if (value.type === 'object' && value.hasOwnProperty('properties')) {
        const customInterface = generateObjectDefinition(
          `${capitalize(name)}${capitalize(key)}`,
          value
        )
        if (Array.isArray(customInterface)) {
          customTypeInterfaces.push(...customInterface)
          return ts.factory.createPropertySignature(
            undefined,
            key,
            undefined,
            ts.factory.createTypeReferenceNode(customInterface.at(-1).name)
          )
        } else {
          // Save it for the node list at this level
          customTypeInterfaces.push(customInterface)
          // Insert a reference to the type in the AST for the root interface
          return ts.factory.createPropertySignature(
            undefined,
            key,
            undefined,
            ts.factory.createTypeReferenceNode(customInterface.name)
          )
        }
      } else {
        return generatePrimitiveDefinition(key, value)
      }
    }
  )
  // Add the root level interface last
  customTypeInterfaces.push(
    ts.factory.createInterfaceDeclaration(
      undefined,
      interfaceExport,
      name,
      undefined,
      undefined,
      interfaceProps
    )
  )
  return ts.factory.createNodeArray(customTypeInterfaces)
}

/**
 * Recursively generate a TypeScript definition for a BIDS schema object
 */
export function generatePrimitiveDefinition(
  name: string,
  definition: Record<string, any>
): Node {
  if (mapSchemaType(definition.type) === 'string') {
    if (definition.hasOwnProperty('enum')) {
      return ts.factory.createPropertySignature(
        undefined,
        name,
        undefined,
        ts.factory.createUnionTypeNode(
          definition.enum.map((enumValue) =>
            ts.factory.createLiteralTypeNode(
              ts.factory.createStringLiteral(mapSchemaType(enumValue))
            )
          )
        )
      )
    } else {
      return ts.factory.createPropertySignature(
        undefined,
        name,
        undefined,
        ts.factory.createTypeReferenceNode('string')
      )
    }
  } else if (mapSchemaType(definition.type) === 'number') {
    return ts.factory.createPropertySignature(
      undefined,
      name,
      undefined,
      ts.factory.createTypeReferenceNode('number')
    )
  } else if (mapSchemaType(definition.type) === 'array') {
    let arrayDefinition = ts.factory.createArrayTypeNode(
      ts.factory.createTypeReferenceNode('any')
    )
    // Typed array case
    if (
      definition.hasOwnProperty('items') &&
      definition.items.hasOwnProperty('type')
    ) {
      arrayDefinition = ts.factory.createArrayTypeNode(
        ts.factory.createTypeReferenceNode(definition.items.type)
      )
    }
    return ts.factory.createPropertySignature(
      undefined,
      name,
      undefined,
      arrayDefinition
    )
  } else if (mapSchemaType(definition.type) === 'object') {
    return ts.factory.createPropertySignature(
      undefined,
      name,
      undefined,
      ts.factory.createTypeReferenceNode('object')
    )
  }
}

/**
 * Given an object like `{ suffix: { type: 'string' } }` return a TypeScript interface
 */
export function generateTypes(schemaObj: Record<string, any>): Array<ts.Node> {
  const tsNodes = []
  for (const prop in schemaObj) {
    if (
      schemaObj[prop].type === 'object' &&
      schemaObj[prop].hasOwnProperty('properties')
    ) {
      tsNodes.push(...generateObjectDefinition(prop, schemaObj[prop]))
    } else {
      tsNodes.push(generatePrimitiveDefinition(prop, schemaObj[prop]))
    }
  }
  return tsNodes
}

export function print(file) {
  // Output formatting
  const printer = ts.createPrinter({
    newLine: ts.NewLineKind.LineFeed,
    omitTrailingSemicolon: true,
  })
  return printer.printFile(file)
}

export function createSourceFile(filename: string) {
  return ts.createSourceFile(
    filename,
    '',
    ts.ScriptTarget.ESNext,
    false,
    ts.ScriptKind.TS
  )
}
