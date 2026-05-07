#!/usr/bin/env node

import { syncToCloud, syncFromCloud, listSynced } from '../lib/sync.mjs';

const args = process.argv.slice(2);
const command = args[0] || 'up';
const flags = args.slice(1);

const dryRun = flags.includes('--dry-run') || flags.includes('-n');
const force = flags.includes('--force') || flags.includes('-f');
const quiet = flags.includes('--quiet') || flags.includes('-q');

async function main() {
  switch (command) {
    case 'up':
    case 'upload':
    case 'push':
      await syncToCloud({ dryRun, force, verbose: !quiet });
      break;

    case 'down':
    case 'download':
    case 'pull':
      await syncFromCloud({ dryRun, verbose: !quiet });
      break;

    case 'list':
    case 'ls':
    case 'status':
      await listSynced(!quiet);
      break;

    case 'help':
    default:
      console.log(`
📦 PubHub Sync - Firebase Storage Sync Tool

Usage: node scripts/sync.mjs <command> [options]

Commands:
  up, upload, push    Upload local files to Firebase Storage
  down, download, pull Download files from Firebase Storage
  list, ls, status    Show sync status and tracked files

Options:
  -n, --dry-run       Preview changes without uploading/downloading
  -f, --force         Force re-upload all files (ignore cache)
  -q, --quiet         Minimal output

Examples:
  node scripts/sync.mjs up              # Upload changed files
  node scripts/sync.mjs up --dry-run    # Preview what would be uploaded
  node scripts/sync.mjs up --force      # Force re-upload everything
  node scripts/sync.mjs down            # Download new remote files
  node scripts/sync.mjs list            # Show sync status
`);
  }
}

main().catch(console.error);
