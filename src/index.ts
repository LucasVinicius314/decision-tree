import * as fs from 'fs'

const filePath: string = 'main.csv'

const main = async () => {
  const then = Date.now()

  try {
    console.info(`Loading ${filePath}...`)

    const fileData = fs.readFileSync(filePath, 'utf8')

    const lines = fileData.split('\n').map((v) => v.split(','))

    const headers = lines.shift()

    if (headers === undefined) {
      throw 'No headers found.'
    }

    const now = Date.now()

    console.info(now - then)

    // console.info(messages.join('\n'))

    console.info('Finished.')
  } catch (err) {
    console.error(err)
  }
}

main()
