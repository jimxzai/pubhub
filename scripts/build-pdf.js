#!/usr/bin/env node

/**
 * PubHub PDF Builder
 * Converts markdown content to PDF using Pandoc + XeLaTeX
 *
 * Usage:
 *   node scripts/build-pdf.js --format journal --input monthly-reports/published/2025-12.md
 *   node scripts/build-pdf.js --format book --input books/sunzi/
 *   node scripts/build-pdf.js --format newspaper --input weekly-summaries/published/2025-12-W4.md
 *   node scripts/build-pdf.js --format brochure --input docs/brochure-content.md
 */

import { execSync, spawn } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const CONFIG = {
  templatesDir: path.join(__dirname, '..', 'templates', 'pdf'),
  outputDir: path.join(__dirname, '..', 'output'),
  formats: {
    journal: {
      template: 'journal.latex',
      engine: 'xelatex',
      description: 'Academic two-column journal layout'
    },
    book: {
      template: 'book.latex',
      engine: 'xelatex',
      description: 'Professional book layout with chapters'
    },
    'gospel-of-john': {
      template: 'gospel-of-john.latex',
      engine: 'xelatex',
      description: 'Professional Gospel of John study book'
    },
    'gospel-of-matthew': {
      template: 'gospel-of-matthew.latex',
      engine: 'xelatex',
      description: 'Professional Gospel of Matthew study book'
    },
    'gospel-of-mark': {
      template: 'gospel-of-mark.latex',
      engine: 'xelatex',
      description: 'Professional Gospel of Mark study book'
    },
    '1-peter': {
      template: '1-peter.latex',
      engine: 'xelatex',
      description: 'Professional 1 Peter study book'
    },
    '2-peter': {
      template: '2-peter.latex',
      engine: 'xelatex',
      description: 'Professional 2 Peter study book'
    },
    'pauline-epistles': {
      template: 'pauline-epistles.latex',
      engine: 'xelatex',
      description: 'Professional Pauline Epistles study book (13 letters)'
    },
    'samuel-chronicles': {
      template: 'samuel-chronicles.latex',
      engine: 'xelatex',
      description: 'Professional Samuel & Chronicles study book with Psalms mapping'
    },
    'james': {
      template: 'james.latex',
      engine: 'xelatex',
      description: 'Professional Epistle of James study book'
    },
    'jude': {
      template: 'jude.latex',
      engine: 'xelatex',
      description: 'Professional Epistle of Jude study book'
    },
    newspaper: {
      template: 'newspaper.css',
      engine: 'html',  // Uses HTML+CSS approach
      description: 'Multi-column newspaper layout'
    },
    brochure: {
      template: 'brochure.css',
      engine: 'html',  // Uses HTML+CSS approach
      description: 'Tri-fold brochure layout'
    }
  }
};

// Parse command line arguments
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    format: 'journal',
    input: null,
    output: null,
    title: null,
    author: null,
    date: null,
    verbose: false,
    help: false
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--format':
      case '-f':
        options.format = args[++i];
        break;
      case '--input':
      case '-i':
        options.input = args[++i];
        break;
      case '--output':
      case '-o':
        options.output = args[++i];
        break;
      case '--title':
      case '-t':
        options.title = args[++i];
        break;
      case '--author':
      case '-a':
        options.author = args[++i];
        break;
      case '--date':
      case '-d':
        options.date = args[++i];
        break;
      case '--verbose':
      case '-v':
        options.verbose = true;
        break;
      case '--help':
      case '-h':
        options.help = true;
        break;
    }
  }

  return options;
}

// Show help message
function showHelp() {
  console.log(`
PubHub PDF Builder - Convert Markdown to Professional PDFs

Usage:
  node scripts/build-pdf.js [options]

Options:
  -f, --format <type>    Output format: journal, book, newspaper, brochure (default: journal)
  -i, --input <path>     Input markdown file or directory
  -o, --output <path>    Output PDF file path (default: output/<filename>.pdf)
  -t, --title <title>    Document title (overrides YAML frontmatter)
  -a, --author <author>  Document author (overrides YAML frontmatter)
  -d, --date <date>      Document date (overrides YAML frontmatter)
  -v, --verbose          Show detailed output
  -h, --help             Show this help message

Formats:
  journal        Academic two-column layout (monthly reports)
  book           Professional book with chapters (final manuscripts)
  gospel-of-john Professional Gospel of John study book (recommended)
  newspaper      Multi-column newspaper layout (weekly summaries)
  brochure       Tri-fold promotional brochure

Examples:
  # Build a journal PDF from monthly report
  node scripts/build-pdf.js -f journal -i monthly-reports/published/2025-12.md

  # Build a book PDF from a directory
  node scripts/build-pdf.js -f book -i books/sunzi/

  # Build a newspaper from weekly summary
  node scripts/build-pdf.js -f newspaper -i weekly-summaries/published/2025-12-W4.md

  # Build with custom metadata
  node scripts/build-pdf.js -f journal -i report.md -t "Custom Title" -a "Author Name"
`);
}

// Ensure output directory exists
function ensureOutputDir() {
  if (!fs.existsSync(CONFIG.outputDir)) {
    fs.mkdirSync(CONFIG.outputDir, { recursive: true });
  }
}

// Check if required tools are installed
function checkDependencies() {
  const required = ['pandoc'];
  const missing = [];

  for (const tool of required) {
    try {
      execSync(`which ${tool}`, { stdio: 'pipe' });
    } catch (error) {
      missing.push(tool);
    }
  }

  if (missing.length > 0) {
    console.error(`Error: Missing required tools: ${missing.join(', ')}`);
    console.error('Please install them first:');
    console.error('  brew install pandoc');
    process.exit(1);
  }
}

// Extract YAML frontmatter from markdown
function extractFrontmatter(content) {
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!frontmatterMatch) return {};

  const yaml = frontmatterMatch[1];
  const metadata = {};

  // Simple YAML parsing for common fields
  const lines = yaml.split('\n');
  for (const line of lines) {
    const match = line.match(/^(\w+):\s*(.+)$/);
    if (match) {
      metadata[match[1]] = match[2].replace(/^["']|["']$/g, '');
    }
  }

  return metadata;
}

// Build PDF using LaTeX engine (journal, book)
function buildWithLatex(options, formatConfig) {
  const templatePath = path.join(CONFIG.templatesDir, formatConfig.template);

  if (!fs.existsSync(templatePath)) {
    console.error(`Error: Template not found: ${templatePath}`);
    process.exit(1);
  }

  const inputPath = path.resolve(options.input);
  const outputPath = options.output || path.join(
    CONFIG.outputDir,
    path.basename(inputPath, '.md') + '.pdf'
  );

  // Read input to extract metadata
  const content = fs.readFileSync(inputPath, 'utf8');
  const metadata = extractFrontmatter(content);

  // Build pandoc command
  const pandocArgs = [
    inputPath,
    '-o', outputPath,
    '--template', templatePath,
    '--pdf-engine', 'xelatex',
    '--pdf-engine-opt', '-interaction=nonstopmode',
    '--toc',
    '--toc-depth=3'
  ];

  // Add metadata
  if (options.title || metadata.title) {
    pandocArgs.push('-V', `title=${options.title || metadata.title}`);
  }
  if (options.author || metadata.author) {
    pandocArgs.push('-V', `author=${options.author || metadata.author}`);
  }
  if (options.date || metadata.date) {
    pandocArgs.push('-V', `date=${options.date || metadata.date}`);
  }

  // Format-specific options
  if (options.format === 'journal') {
    pandocArgs.push('-V', 'journal-name=PubHub Journal');
  }

  console.log(`Building ${options.format} PDF...`);
  if (options.verbose) {
    console.log(`Command: pandoc ${pandocArgs.join(' ')}`);
  }

  try {
    execSync(`pandoc ${pandocArgs.map(a => `"${a}"`).join(' ')}`, {
      stdio: options.verbose ? 'inherit' : 'pipe',
      cwd: path.dirname(inputPath)
    });
    console.log(`✓ PDF generated: ${outputPath}`);
    return outputPath;
  } catch (error) {
    console.error('Error generating PDF:', error.message);
    if (!options.verbose) {
      console.error('Run with --verbose for more details');
    }
    process.exit(1);
  }
}

// Build PDF using HTML+CSS engine (newspaper, brochure)
function buildWithHtml(options, formatConfig) {
  const cssPath = path.join(CONFIG.templatesDir, formatConfig.template);

  if (!fs.existsSync(cssPath)) {
    console.error(`Error: CSS template not found: ${cssPath}`);
    process.exit(1);
  }

  const inputPath = path.resolve(options.input);
  const outputPath = options.output || path.join(
    CONFIG.outputDir,
    path.basename(inputPath, '.md') + '.pdf'
  );
  const htmlPath = outputPath.replace('.pdf', '.html');

  // Read input to extract metadata
  const content = fs.readFileSync(inputPath, 'utf8');
  const metadata = extractFrontmatter(content);

  // First convert to HTML
  const pandocHtmlArgs = [
    inputPath,
    '-o', htmlPath,
    '--standalone',
    '--css', cssPath,
    '--embed-resources',
    '--metadata', `title=${options.title || metadata.title || 'PubHub'}`,
  ];

  console.log(`Building ${options.format} PDF via HTML...`);

  try {
    // Step 1: Generate HTML
    execSync(`pandoc ${pandocHtmlArgs.map(a => `"${a}"`).join(' ')}`, {
      stdio: options.verbose ? 'inherit' : 'pipe',
      cwd: path.dirname(inputPath)
    });

    // Step 2: Convert HTML to PDF
    // Try wkhtmltopdf first, fall back to browser-based solution
    let pdfSuccess = false;

    // Try wkhtmltopdf
    try {
      execSync('which wkhtmltopdf', { stdio: 'pipe' });
      const wkArgs = [
        '--enable-local-file-access',
        '--page-size', 'A4',
        options.format === 'brochure' ? '--orientation' : '--orientation',
        options.format === 'brochure' ? 'Landscape' : 'Portrait',
        htmlPath,
        outputPath
      ];
      execSync(`wkhtmltopdf ${wkArgs.join(' ')}`, {
        stdio: options.verbose ? 'inherit' : 'pipe'
      });
      pdfSuccess = true;
    } catch (wkError) {
      if (options.verbose) {
        console.log('wkhtmltopdf not available, trying alternative...');
      }
    }

    // Try pandoc with weasyprint if wkhtmltopdf failed
    if (!pdfSuccess) {
      try {
        execSync(`pandoc "${htmlPath}" -o "${outputPath}" --pdf-engine=weasyprint`, {
          stdio: options.verbose ? 'inherit' : 'pipe'
        });
        pdfSuccess = true;
      } catch (wpError) {
        if (options.verbose) {
          console.log('WeasyPrint not available...');
        }
      }
    }

    // Final fallback: use pandoc with default engine
    if (!pdfSuccess) {
      console.log('Note: For best results with newspaper/brochure format, install wkhtmltopdf or weasyprint');
      execSync(`pandoc "${inputPath}" -o "${outputPath}" --pdf-engine=xelatex`, {
        stdio: options.verbose ? 'inherit' : 'pipe'
      });
    }

    // Clean up HTML file
    if (fs.existsSync(htmlPath) && !options.verbose) {
      fs.unlinkSync(htmlPath);
    }

    console.log(`✓ PDF generated: ${outputPath}`);
    return outputPath;
  } catch (error) {
    console.error('Error generating PDF:', error.message);
    if (!options.verbose) {
      console.error('Run with --verbose for more details');
    }
    process.exit(1);
  }
}

// Build from directory (for book format)
function buildFromDirectory(options) {
  const dirPath = path.resolve(options.input);

  if (!fs.existsSync(dirPath) || !fs.statSync(dirPath).isDirectory()) {
    console.error(`Error: Directory not found: ${dirPath}`);
    process.exit(1);
  }

  // Find all markdown files in order
  const files = fs.readdirSync(dirPath)
    .filter(f => f.endsWith('.md') && !f.startsWith('README'))
    .sort()
    .map(f => path.join(dirPath, f));

  if (files.length === 0) {
    console.error('Error: No markdown files found in directory');
    process.exit(1);
  }

  // Create combined markdown file
  const combinedPath = path.join(CONFIG.outputDir, 'combined-book.md');
  let combinedContent = '';

  for (const file of files) {
    const content = fs.readFileSync(file, 'utf8');
    combinedContent += content + '\n\n';
  }

  fs.writeFileSync(combinedPath, combinedContent);

  // Build PDF from combined file
  const originalInput = options.input;
  options.input = combinedPath;
  const result = buildWithLatex(options, CONFIG.formats[options.format]);

  // Clean up
  fs.unlinkSync(combinedPath);
  options.input = originalInput;

  return result;
}

// Main function
function main() {
  const options = parseArgs();

  if (options.help) {
    showHelp();
    process.exit(0);
  }

  if (!options.input) {
    console.error('Error: Input file or directory required. Use --help for usage.');
    process.exit(1);
  }

  if (!CONFIG.formats[options.format]) {
    console.error(`Error: Unknown format '${options.format}'`);
    console.error(`Available formats: ${Object.keys(CONFIG.formats).join(', ')}`);
    process.exit(1);
  }

  checkDependencies();
  ensureOutputDir();

  const formatConfig = CONFIG.formats[options.format];
  const inputStat = fs.statSync(options.input);

  console.log(`\n📄 PubHub PDF Builder`);
  console.log(`   Format: ${options.format} (${formatConfig.description})`);
  console.log(`   Input:  ${options.input}`);
  console.log('');

  if (inputStat.isDirectory()) {
    const dirFormats = ['book', 'samuel-chronicles', 'gospel-of-john', 'gospel-of-matthew', 'gospel-of-mark', '1-peter', '2-peter', 'pauline-epistles', 'james'];
    if (!dirFormats.includes(options.format)) {
      console.error('Error: Directory input only supported for book-style formats');
      process.exit(1);
    }
    buildFromDirectory(options);
  } else {
    if (formatConfig.engine === 'xelatex') {
      buildWithLatex(options, formatConfig);
    } else {
      buildWithHtml(options, formatConfig);
    }
  }

  console.log('\n✅ Build complete!\n');
}

// Run
main();
