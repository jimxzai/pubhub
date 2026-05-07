#!/usr/bin/env node

/**
 * Publish to Cloud - Upload published content to Firebase Storage
 *
 * Usage:
 *   node scripts/publish-to-cloud.mjs weekly    # Upload latest weekly summary
 *   node scripts/publish-to-cloud.mjs monthly   # Upload latest monthly report
 *   node scripts/publish-to-cloud.mjs pdf <file> # Upload a PDF file
 *   node scripts/publish-to-cloud.mjs all       # Upload all published content
 */

import fs from 'fs';
import path from 'path';
import { uploadFile, uploadText, listFiles, getFileUrl } from '../lib/firebase.mjs';

const PROJECT_ROOT = path.resolve(new URL('.', import.meta.url).pathname, '..');

const PUBLISH_PATHS = {
  weekly: {
    local: 'weekly-summaries/published',
    remote: 'published/weekly',
    pattern: /^\d{4}-\d{2}-W\d+\.md$/
  },
  monthly: {
    local: 'monthly-reports/published',
    remote: 'published/monthly',
    pattern: /^\d{4}-\d{2}\.md$/
  },
  daily: {
    local: 'daily-notes/published',
    remote: 'published/daily',
    pattern: /^\d{4}-\d{2}-\d{2}\.md$/
  },
  pdf: {
    local: 'output',
    remote: 'published/pdf',
    pattern: /\.pdf$/
  },
  books: {
    local: 'books',
    remote: 'published/books',
    pattern: /\.md$/
  }
};

// Get the latest file matching a pattern
function getLatestFile(dir, pattern) {
  if (!fs.existsSync(dir)) return null;

  const files = fs.readdirSync(dir)
    .filter(f => pattern.test(f))
    .map(f => ({
      name: f,
      path: path.join(dir, f),
      mtime: fs.statSync(path.join(dir, f)).mtime
    }))
    .sort((a, b) => b.mtime - a.mtime);

  return files[0] || null;
}

// Get all files matching a pattern
function getAllFiles(dir, pattern, recursive = true) {
  const files = [];
  if (!fs.existsSync(dir)) return files;

  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory() && recursive) {
      files.push(...getAllFiles(fullPath, pattern, recursive));
    } else if (entry.isFile() && pattern.test(entry.name)) {
      files.push({
        name: entry.name,
        path: fullPath,
        relativePath: path.relative(dir, fullPath)
      });
    }
  }
  return files;
}

// Upload a single file
async function publishFile(localPath, remotePath, verbose = true) {
  const content = fs.readFileSync(localPath);
  const ext = path.extname(localPath).toLowerCase();

  const contentType = {
    '.md': 'text/markdown',
    '.pdf': 'application/pdf',
    '.txt': 'text/plain',
    '.json': 'application/json',
    '.html': 'text/html'
  }[ext] || 'application/octet-stream';

  try {
    const url = await uploadFile(remotePath, content, { contentType });
    if (verbose) {
      console.log(`✅ Published: ${remotePath}`);
      console.log(`   URL: ${url}`);
    }
    return { success: true, url, path: remotePath };
  } catch (error) {
    if (verbose) console.log(`❌ Failed: ${remotePath} - ${error.message}`);
    return { success: false, error: error.message, path: remotePath };
  }
}

// Commands
async function publishWeekly(verbose = true) {
  const config = PUBLISH_PATHS.weekly;
  const localDir = path.join(PROJECT_ROOT, config.local);
  const latest = getLatestFile(localDir, config.pattern);

  if (!latest) {
    console.log('❌ No weekly summaries found to publish');
    return null;
  }

  if (verbose) console.log(`📤 Publishing latest weekly summary: ${latest.name}`);
  return publishFile(latest.path, `${config.remote}/${latest.name}`, verbose);
}

async function publishMonthly(verbose = true) {
  const config = PUBLISH_PATHS.monthly;
  const localDir = path.join(PROJECT_ROOT, config.local);
  const latest = getLatestFile(localDir, config.pattern);

  if (!latest) {
    console.log('❌ No monthly reports found to publish');
    return null;
  }

  if (verbose) console.log(`📤 Publishing latest monthly report: ${latest.name}`);
  return publishFile(latest.path, `${config.remote}/${latest.name}`, verbose);
}

async function publishPdf(filePath, verbose = true) {
  if (!filePath || !fs.existsSync(filePath)) {
    console.log('❌ PDF file not found:', filePath);
    return null;
  }

  const fileName = path.basename(filePath);
  if (verbose) console.log(`📤 Publishing PDF: ${fileName}`);
  return publishFile(filePath, `${PUBLISH_PATHS.pdf.remote}/${fileName}`, verbose);
}

async function publishAll(verbose = true) {
  console.log('📤 Publishing all content to Firebase Storage...\n');
  const results = { success: [], failed: [] };

  for (const [type, config] of Object.entries(PUBLISH_PATHS)) {
    const localDir = path.join(PROJECT_ROOT, config.local);
    const files = getAllFiles(localDir, config.pattern);

    if (files.length === 0) continue;

    console.log(`\n📁 ${type} (${files.length} files)`);

    for (const file of files) {
      const remotePath = `${config.remote}/${file.relativePath || file.name}`;
      const result = await publishFile(file.path, remotePath, verbose);
      if (result.success) {
        results.success.push(result);
      } else {
        results.failed.push(result);
      }
    }
  }

  console.log(`\n📊 Summary:`);
  console.log(`   Published: ${results.success.length}`);
  console.log(`   Failed: ${results.failed.length}`);

  return results;
}

async function listPublished(verbose = true) {
  console.log('📋 Published content in Firebase Storage:\n');

  for (const [type, config] of Object.entries(PUBLISH_PATHS)) {
    try {
      const { files } = await listFiles(config.remote);
      if (files.length > 0) {
        console.log(`📁 ${type}:`);
        for (const file of files) {
          const url = await getFileUrl(file);
          console.log(`   - ${path.basename(file)}`);
          if (verbose) console.log(`     ${url}`);
        }
      }
    } catch {
      // Folder doesn't exist yet
    }
  }
}

// Main
async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'help';

  switch (command) {
    case 'weekly':
      await publishWeekly();
      break;
    case 'monthly':
      await publishMonthly();
      break;
    case 'pdf':
      await publishPdf(args[1]);
      break;
    case 'all':
      await publishAll();
      break;
    case 'list':
      await listPublished();
      break;
    case 'help':
    default:
      console.log(`
📚 Publish to Cloud - Upload published content to Firebase Storage

Usage: node scripts/publish-to-cloud.mjs <command> [options]

Commands:
  weekly     Upload the latest weekly summary
  monthly    Upload the latest monthly report
  pdf <file> Upload a specific PDF file
  all        Upload all published content
  list       List all published content in cloud

Examples:
  node scripts/publish-to-cloud.mjs weekly
  node scripts/publish-to-cloud.mjs pdf output/report.pdf
  node scripts/publish-to-cloud.mjs all
`);
  }
}

main().catch(console.error);
