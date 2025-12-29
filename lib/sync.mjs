#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { uploadFile, getFileUrl, listFiles, deleteFile } from './firebase.mjs';

const PROJECT_ROOT = path.resolve(new URL('.', import.meta.url).pathname, '..');
const SYNC_STATE_FILE = path.join(PROJECT_ROOT, '.sync-state.json');

// Folders to sync (relative to project root)
const SYNC_FOLDERS = [
  { local: 'daily-notes/published', remote: 'notes/published' },
  { local: 'daily-notes/drafts', remote: 'notes/drafts' },
  { local: 'books/sunzi', remote: 'books/sunzi' },
  { local: 'books/bible', remote: 'books/bible' },
  { local: 'books/zizhi-tongjian', remote: 'books/zizhi-tongjian' },
];

// File extensions to sync
const SYNC_EXTENSIONS = ['.md', '.pdf', '.txt', '.json'];

// Load sync state (tracks what's been uploaded)
function loadSyncState() {
  try {
    return JSON.parse(fs.readFileSync(SYNC_STATE_FILE, 'utf-8'));
  } catch {
    return { files: {}, lastSync: null };
  }
}

// Save sync state
function saveSyncState(state) {
  state.lastSync = new Date().toISOString();
  fs.writeFileSync(SYNC_STATE_FILE, JSON.stringify(state, null, 2));
}

// Get file hash
function getFileHash(filePath) {
  const content = fs.readFileSync(filePath);
  return crypto.createHash('md5').update(content).digest('hex');
}

// Get all files in a directory recursively
function getLocalFiles(dir, baseDir = dir) {
  const files = [];
  if (!fs.existsSync(dir)) return files;

  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      // Skip hidden folders and node_modules
      if (!entry.name.startsWith('.') && entry.name !== 'node_modules') {
        files.push(...getLocalFiles(fullPath, baseDir));
      }
    } else if (SYNC_EXTENSIONS.includes(path.extname(entry.name).toLowerCase())) {
      files.push({
        localPath: fullPath,
        relativePath: path.relative(baseDir, fullPath),
        hash: getFileHash(fullPath),
        size: fs.statSync(fullPath).size,
        modified: fs.statSync(fullPath).mtime.toISOString()
      });
    }
  }
  return files;
}

// Upload a single file
async function uploadLocalFile(localPath, remotePath) {
  const content = fs.readFileSync(localPath);
  const ext = path.extname(localPath).toLowerCase();
  const contentType = {
    '.md': 'text/markdown',
    '.pdf': 'application/pdf',
    '.txt': 'text/plain',
    '.json': 'application/json'
  }[ext] || 'application/octet-stream';

  return uploadFile(remotePath, content, { contentType });
}

// Sync local files to cloud
export async function syncToCloud(options = {}) {
  const { dryRun = false, force = false, verbose = true } = options;
  const state = loadSyncState();
  const results = { uploaded: [], skipped: [], errors: [] };

  if (verbose) console.log('🔄 Starting sync to Firebase Storage...\n');

  for (const folder of SYNC_FOLDERS) {
    const localDir = path.join(PROJECT_ROOT, folder.local);
    const files = getLocalFiles(localDir);

    if (verbose && files.length > 0) {
      console.log(`📁 ${folder.local} (${files.length} files)`);
    }

    for (const file of files) {
      const remotePath = `${folder.remote}/${file.relativePath}`;
      const stateKey = remotePath;
      const existingHash = state.files[stateKey]?.hash;

      // Skip if unchanged (unless force)
      if (!force && existingHash === file.hash) {
        results.skipped.push(remotePath);
        continue;
      }

      if (dryRun) {
        if (verbose) console.log(`   [DRY] Would upload: ${file.relativePath}`);
        results.uploaded.push(remotePath);
        continue;
      }

      try {
        const url = await uploadLocalFile(file.localPath, remotePath);
        state.files[stateKey] = {
          hash: file.hash,
          size: file.size,
          uploaded: new Date().toISOString(),
          url
        };
        results.uploaded.push(remotePath);
        if (verbose) console.log(`   ✅ ${file.relativePath}`);
      } catch (error) {
        results.errors.push({ path: remotePath, error: error.message });
        if (verbose) console.log(`   ❌ ${file.relativePath}: ${error.message}`);
      }
    }
  }

  if (!dryRun) saveSyncState(state);

  if (verbose) {
    console.log(`\n📊 Summary:`);
    console.log(`   Uploaded: ${results.uploaded.length}`);
    console.log(`   Skipped:  ${results.skipped.length} (unchanged)`);
    console.log(`   Errors:   ${results.errors.length}`);
  }

  return results;
}

// Download files from cloud to local
export async function syncFromCloud(options = {}) {
  const { dryRun = false, verbose = true } = options;
  const results = { downloaded: [], skipped: [], errors: [] };

  if (verbose) console.log('⬇️  Starting download from Firebase Storage...\n');

  for (const folder of SYNC_FOLDERS) {
    try {
      const { files } = await listFiles(folder.remote);
      if (verbose && files.length > 0) {
        console.log(`📁 ${folder.remote} (${files.length} files)`);
      }

      for (const remotePath of files) {
        const relativePath = remotePath.replace(`${folder.remote}/`, '');
        const localPath = path.join(PROJECT_ROOT, folder.local, relativePath);

        // Create directory if needed
        const localDir = path.dirname(localPath);
        if (!dryRun && !fs.existsSync(localDir)) {
          fs.mkdirSync(localDir, { recursive: true });
        }

        // Skip if local file exists (could add hash comparison)
        if (fs.existsSync(localPath)) {
          results.skipped.push(remotePath);
          continue;
        }

        if (dryRun) {
          if (verbose) console.log(`   [DRY] Would download: ${relativePath}`);
          results.downloaded.push(remotePath);
          continue;
        }

        try {
          const url = await getFileUrl(remotePath);
          const response = await fetch(url);
          const content = await response.arrayBuffer();
          fs.writeFileSync(localPath, Buffer.from(content));
          results.downloaded.push(remotePath);
          if (verbose) console.log(`   ✅ ${relativePath}`);
        } catch (error) {
          results.errors.push({ path: remotePath, error: error.message });
          if (verbose) console.log(`   ❌ ${relativePath}: ${error.message}`);
        }
      }
    } catch (error) {
      if (verbose) console.log(`   ⚠️  Could not list ${folder.remote}: ${error.message}`);
    }
  }

  if (verbose) {
    console.log(`\n📊 Summary:`);
    console.log(`   Downloaded: ${results.downloaded.length}`);
    console.log(`   Skipped:    ${results.skipped.length} (already exists)`);
    console.log(`   Errors:     ${results.errors.length}`);
  }

  return results;
}

// List all synced files
export async function listSynced(verbose = true) {
  const state = loadSyncState();
  const files = Object.entries(state.files);

  if (verbose) {
    console.log(`📋 Synced files (${files.length} total):\n`);
    for (const [path, info] of files) {
      console.log(`   ${path}`);
      console.log(`      Size: ${(info.size / 1024).toFixed(1)}KB | Uploaded: ${info.uploaded}`);
    }
    if (state.lastSync) {
      console.log(`\n🕐 Last sync: ${state.lastSync}`);
    }
  }

  return state;
}

export { SYNC_FOLDERS, PROJECT_ROOT };
