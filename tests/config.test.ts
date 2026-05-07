import { describe, it, expect } from 'vitest'
import { readFileSync } from 'fs'
import { join } from 'path'

describe('Project Configuration', () => {
  describe('package.json', () => {
    const pkg = JSON.parse(
      readFileSync(join(process.cwd(), 'package.json'), 'utf-8')
    )

    it('should have correct project name', () => {
      expect(pkg.name).toBe('three-books-publishing')
    })

    it('should use pnpm as package manager', () => {
      expect(pkg.packageManager).toMatch(/^pnpm@/)
    })

    it('should have Next.js 16.x dependency', () => {
      expect(pkg.dependencies.next).toMatch(/^\^16\./)
    })

    it('should have React 19.x dependency', () => {
      expect(pkg.dependencies.react).toMatch(/^\^19\./)
    })

    it('should have required scripts', () => {
      expect(pkg.scripts).toHaveProperty('dev')
      expect(pkg.scripts).toHaveProperty('build')
      expect(pkg.scripts).toHaveProperty('start')
      expect(pkg.scripts).toHaveProperty('lint')
      expect(pkg.scripts).toHaveProperty('typecheck')
    })
  })

  describe('.claude/settings.json', () => {
    const settings = JSON.parse(
      readFileSync(join(process.cwd(), '.claude/settings.json'), 'utf-8')
    )

    it('should have MVP configuration', () => {
      expect(settings.mvp).toBeDefined()
      expect(settings.mvp.name).toBe('Gospel of John Study')
    })

    it('should have correct core resources', () => {
      const { coreResources } = settings.mvp
      expect(coreResources.elderWong).toBeDefined()
      expect(coreResources.gty).toBeDefined()
      expect(coreResources.campbellMorgan).toBeDefined()
    })

    it('should have bible versions configured', () => {
      const { bibleVersions } = settings.mvp
      expect(bibleVersions.chinese.primary).toBe('和合本修訂版 (RCUV)')
      expect(bibleVersions.english.primary).toBe('ESV (English Standard Version)')
    })

    it('should have daily rhythm configured', () => {
      const { dailyRhythm } = settings.mvp
      expect(dailyRhythm.morning).toBeDefined()
      expect(dailyRhythm.evening).toBeDefined()
      expect(dailyRhythm.morning.steps).toHaveLength(6)
    })

    it('should have tech stack configured', () => {
      expect(settings.techStack.framework).toBe('Next.js 16.1')
      expect(settings.techStack.packageManager).toBe('pnpm')
    })

    it('should have Gospel of John structure', () => {
      const johnContext = settings.contextRules.bookContext['gospel-of-john']
      expect(johnContext.chapters).toBe(21)
      expect(johnContext.themes.sevenSigns).toHaveLength(7)
      expect(johnContext.themes.sevenIAm).toHaveLength(7)
    })
  })
})

describe('MVP Content Validation', () => {
  const settings = JSON.parse(
    readFileSync(join(process.cwd(), '.claude/settings.json'), 'utf-8')
  )

  it('should have 7 Signs of John', () => {
    const signs = settings.contextRules.bookContext['gospel-of-john'].themes.sevenSigns
    expect(signs).toContain('水變酒')
    expect(signs).toContain('拉撒路復活')
  })

  it('should have 7 I AM statements', () => {
    const iAm = settings.contextRules.bookContext['gospel-of-john'].themes.sevenIAm
    expect(iAm).toContain('生命的糧')
    expect(iAm).toContain('世界的光')
    expect(iAm).toContain('好牧人')
    expect(iAm).toContain('真葡萄樹')
  })

  it('should have Elder Wong as priority 1 resource', () => {
    expect(settings.mvp.coreResources.elderWong.priority).toBe(1)
  })

  it('should have gty.org URL configured', () => {
    expect(settings.mvp.coreResources.gty.url).toBe('https://www.gty.org')
  })
})
