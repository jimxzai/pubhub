/**
 * md-to-pdf 配置文件
 *
 * 安裝: npm install -g md-to-pdf
 * 使用: md-to-pdf books/hebrews-study-guide.md
 */

module.exports = {
  // PDF 選項
  pdf_options: {
    format: 'A4',
    margin: {
      top: '2.5cm',
      bottom: '2.5cm',
      left: '2.5cm',
      right: '2.5cm'
    },
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: `
      <div style="font-size: 9pt; color: #888; width: 100%; text-align: center; padding-top: 5mm;">
        七年三書精讀出版系統
      </div>
    `,
    footerTemplate: `
      <div style="font-size: 9pt; color: #888; width: 100%; text-align: center; padding-bottom: 5mm;">
        <span class="pageNumber"></span> / <span class="totalPages"></span>
      </div>
    `
  },

  // 樣式表
  stylesheet: 'templates/pdf-style.css',

  // 自定義 CSS
  css: `
    body {
      font-family: "Noto Serif CJK TC", "Source Han Serif TC", serif;
    }
  `,

  // 語法高亮主題
  highlight_style: 'github',

  // Markdown 選項
  marked_options: {
    headerIds: true,
    smartypants: true
  },

  // 輸出目錄
  dest: 'books/',

  // 文件名後綴
  // 自動將 .md 替換為 .pdf

  // 啟動瀏覽器選項
  launch_options: {
    headless: true
  }
};
