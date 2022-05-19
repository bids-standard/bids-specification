import { assertEquals } from 'https://deno.land/std@0.138.0/testing/asserts.ts'
import { toCamel, generateTypes, print, createSourceFile } from './generate.ts'

Deno.test('toCamel() supports expected specification names', () => {
  assertEquals(toCamel('dim_info'), 'DimInfo')
  assertEquals(toCamel('dataset'), 'Dataset')
  assertEquals(toCamel('Dataset_nifti_PixDim'), 'DatasetNiftiPixDim')
})

Deno.test('generateTypes() supports primitive string', () => {
  const file = createSourceFile('test.ts')
  file.statements = generateTypes({
    suffix: { description: 'Suffix of current file', type: 'string' },
  })

  assertEquals(print(file), 'suffix: string;\n')
})

Deno.test('generateTypes() supports enumerated string', () => {
  const file = createSourceFile('test.ts')
  file.statements = generateTypes({
    t: {
      name: 'Time Unit',
      description: 'String representing the unit of inter-volume intervals.',
      type: 'string',
      enum: ['unknown', 'sec', 'msec', 'usec'],
    },
  })

  assertEquals(print(file), 't: "unknown" | "sec" | "msec" | "usec";\n')
})

Deno.test('generateTypes() supports primitive integer', () => {
  const file = createSourceFile('test.ts')
  file.statements = generateTypes({
    n_cols: { description: 'Number of columns in bvec file', type: 'integer' },
  })

  assertEquals(print(file), 'n_cols: number;\n')
})

// This is an array with no schema defined type
Deno.test('generateTypes() supports generic array type', () => {
  const file = createSourceFile('test.ts')
  file.statements = generateTypes({
    ignored: { description: 'Set of ignored files', type: 'array' },
  })

  assertEquals(print(file), 'ignored: any[];\n')
})

// This is an array with a schema defined type
Deno.test('generateTypes() supports typed array type', () => {
  const file = createSourceFile('test.ts')
  file.statements = generateTypes({
    sub_dirs: {
      description: 'Subjects as determined by sub-*/ directories',
      type: 'array',
      items: { type: 'string' },
    },
  })

  assertEquals(print(file), 'sub_dirs: string[];\n')
})

// Object without defined properties
Deno.test('generateTypes() supports generic object type', () => {
  const file = createSourceFile('test.ts')
  file.statements = generateTypes({
    dataset_description: {
      description: 'Contents of /dataset_description.json',
      type: 'object',
    },
  })

  assertEquals(print(file), 'dataset_description: object;\n')
})

// Object with defined properties
Deno.test('generateTypes() supports typed object type', () => {
  const file = createSourceFile('test.ts')
  file.statements = generateTypes({
    dim_info: {
      name: 'Dimension Information',
      description: 'Metadata about dimensions data.',
      type: 'object',
      properties: {
        freq: {
          name: 'Frequency',
          description:
            'These fields encode which spatial dimension (1, 2, or 3).',
          type: 'integer',
        },
        phase: {
          name: 'Phase',
          description:
            'Corresponds to which acquisition dimension for MRI data.',
          type: 'integer',
        },
        slice: {
          name: 'Slice',
          description: 'Slice dimensions.',
          type: 'integer',
        },
      },
    },
  })

  assertEquals(
    print(file),
    `export interface DimInfo {
    freq: number;
    phase: number;
    slice: number;
}
`
  )
})

// Works with complex object trees
// Object with defined properties
Deno.test('generateTypes() supports object trees', () => {
  const file = createSourceFile('test.ts')
  file.statements = generateTypes({
    dataset: {
      description: 'Test dataset fragment',
      type: 'object',
      properties: {
        dataset_description: {
          description: 'Contents of /dataset_description.json',
          type: 'object',
        },
        subjects: {
          description: 'Collections of subjects in dataset',
          type: 'object',
          properties: {
            sub_dirs: {
              description: 'Subjects as determined by sub-*/ directories',
              type: 'array',
              items: { type: 'string' },
            },
          },
        },
      },
    },
  })

  assertEquals(
    print(file),
    `export interface DatasetSubjects {
    sub_dirs: string[];
}
export interface Dataset {
    dataset_description: object;
    subjects: DatasetSubjects;
}
`
  )
})
