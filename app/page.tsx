export default function Home() {
  return (
    <main className="min-h-screen p-8 max-w-4xl mx-auto">
      <header className="mb-12">
        <h1 className="text-4xl font-bold text-primary-900 mb-2">
          生命之道
        </h1>
        <p className="text-xl text-primary-700">
          約翰福音研讀 | Gospel of John Study
        </p>
      </header>

      <section className="mb-8">
        <blockquote className="scripture-quote text-lg">
          <p className="chinese-text mb-2">
            「太初有道，道與神同在，道就是神。」
          </p>
          <p className="english-text text-gray-600">
            "In the beginning was the Word, and the Word was with God, and the Word was God."
          </p>
          <cite className="block mt-2 text-sm text-gray-500">
            — 約翰福音 1:1 (John 1:1)
          </cite>
        </blockquote>
      </section>

      <section className="grid md:grid-cols-3 gap-6 mb-12">
        <div className="p-6 bg-primary-50 rounded-lg">
          <h2 className="font-bold text-lg mb-2">黃長老教導</h2>
          <p className="text-sm text-gray-600">
            週四查經班現場教導，第一手屬靈餵養
          </p>
        </div>
        <div className="p-6 bg-primary-50 rounded-lg">
          <h2 className="font-bold text-lg mb-2">gty.org</h2>
          <p className="text-sm text-gray-600">
            John MacArthur 逐節解經，忠於原文
          </p>
        </div>
        <div className="p-6 bg-primary-50 rounded-lg">
          <h2 className="font-bold text-lg mb-2">Campbell Morgan</h2>
          <p className="text-sm text-gray-600">
            解經王子，屬靈組織分析法
          </p>
        </div>
      </section>

      <section className="prose prose-primary max-w-none">
        <h2>MVP 原則</h2>
        <p className="text-lg font-medium text-primary-800">
          "Truly Go Deeper" — 寧深不廣，在約翰福音一卷書中扎根
        </p>

        <h3>每日靈修節奏</h3>
        <ul>
          <li>📖 早晨 45-60分鐘：經文、教導、洞見、筆記</li>
          <li>🌙 晚間 15分鐘：回顧、反思、禱告</li>
        </ul>
      </section>

      <footer className="mt-16 pt-8 border-t text-center text-sm text-gray-500">
        <p>7年三書精讀出版系統 | 2025-2032</p>
        <p className="mt-1">Built with Next.js 16.1 + Turbopack + pnpm</p>
      </footer>
    </main>
  )
}
