export const partialEntropy = (v: number) => {
  const value = -v * Math.log2(v)

  return Number.isNaN(value) ? 0 : value
}

export const entropy = (a: number, b: number) =>
  partialEntropy(a) + partialEntropy(b)
