import * as fs from 'fs'

import { filePath, skipColumnLabels } from './utils/config'

import { entropy } from './utils/utils'

const main = async () => {
  const then = Date.now()

  try {
    console.info(`Loading ${filePath}...`)

    const fileData = fs.readFileSync(filePath, 'utf8').replaceAll('\r', '')

    const lines = fileData.split('\n').map((v) => v.split(','))

    const headers = lines.shift()

    if (headers === undefined) {
      throw 'No headers found.'
    }

    const targetColumnIndex = headers.length - 1

    const targetValues = lines
      .map((v) => v[targetColumnIndex])
      .reduce<{
        [key: string]: number
      }>((previousValue, currentValue, currentIndex, array) => {
        previousValue[currentValue] = (previousValue[currentValue] ?? 0) + 1

        return previousValue
      }, {})

    const entries = Object.entries(targetValues)

    const one = entries[0][1]
    const two = entries[1][1]

    const sum = one + two

    const maxEntropy = entropy(one / sum, two / sum)

    console.info(`max entropy: ${maxEntropy}`)

    const columnGains = headers
      .map((headerLabel, headerIndex) => {
        if (skipColumnLabels.includes(headerLabel)) {
          return
        }

        const valuesAbsoluteFrequencyMap = lines
          .map((v2) => v2[headerIndex])
          .reduce<{
            [key: string]: number
          }>((previousValue, currentValue, currentIndex, array) => {
            previousValue[currentValue] = (previousValue[currentValue] ?? 0) + 1

            return previousValue
          }, {})

        const data = Object.entries(valuesAbsoluteFrequencyMap).map(
          (valueLabelEntry) => {
            const valueLabel = valueLabelEntry[0]
            const absoluteFrequency = valueLabelEntry[1]
            const relativeFrequency = absoluteFrequency / lines.length

            const ones = lines.filter(
              (f) =>
                f[headerIndex] === valueLabel &&
                f[targetColumnIndex] === entries[0][0]
            ).length

            const twos = lines.filter(
              (f) =>
                f[headerIndex] === valueLabel &&
                f[targetColumnIndex] === entries[1][0]
            ).length

            const localEntropy =
              relativeFrequency *
              entropy(ones / absoluteFrequency, twos / absoluteFrequency)

            return {
              debugLabel: `\n  ${valueLabel}:\n    abs. freq: ${absoluteFrequency}\n    rel. freq: ${relativeFrequency}\n    entropy: ${localEntropy}`,
              relativeFrequency: relativeFrequency,
              localEntropy: localEntropy,
            }
          }
        )

        const entropySum = data
          .map((v) => v.localEntropy)
          .reduce((a, b) => a + b)
        const gain = maxEntropy - entropySum

        console.log(
          `column ${headerLabel}:\n    (entropy sum: ${entropySum})\n    (gain: ${gain})${data
            .map((v) => v.debugLabel)
            .join('\n')}\n`
        )

        return {
          headerLabel,
          gain,
        }
      })
      .sort((a, b) => (b?.gain ?? 0) - (a?.gain ?? 0))
      .filter((f) => f?.headerLabel !== headers[targetColumnIndex])

    console.log(columnGains)

    const targetColumn = columnGains[0]

    console.info(targetColumn)

    const now = Date.now()

    console.info(now - then)

    // console.info(messages.join('\n'))

    console.info('Finished.')
  } catch (err) {
    console.error(err)
  }
}

main()
