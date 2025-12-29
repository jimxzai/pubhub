#!/usr/bin/env node

import { uploadText, getFileUrl, listFiles, deleteFile } from '../lib/firebase.mjs';

async function testFirebaseStorage() {
  console.log('🔥 Testing Firebase Storage connection...\n');

  const testPath = 'test/connection-test.txt';
  const testContent = `Firebase Storage test - ${new Date().toISOString()}`;

  try {
    // Test 1: Upload
    console.log('1️⃣  Uploading test file...');
    const uploadUrl = await uploadText(testPath, testContent);
    console.log(`   ✅ Uploaded: ${uploadUrl}\n`);

    // Test 2: Get URL
    console.log('2️⃣  Getting download URL...');
    const url = await getFileUrl(testPath);
    console.log(`   ✅ URL: ${url}\n`);

    // Test 3: List files
    console.log('3️⃣  Listing files in test/...');
    const { files, folders } = await listFiles('test');
    console.log(`   ✅ Found ${files.length} file(s), ${folders.length} folder(s)`);
    files.forEach(f => console.log(`      - ${f}`));
    console.log();

    // Test 4: Cleanup
    console.log('4️⃣  Cleaning up test file...');
    await deleteFile(testPath);
    console.log('   ✅ Deleted test file\n');

    console.log('🎉 All tests passed! Firebase Storage is working.');

  } catch (error) {
    console.error('❌ Test failed:', error.message);
    console.error('   Code:', error.code);
    console.error('   Full error:', JSON.stringify(error, null, 2));
    if (error.serverResponse) {
      console.error('   Server response:', error.serverResponse);
    }
    console.error('\n💡 Check:');
    console.error('   1. Firebase Storage is enabled in console');
    console.error('   2. Storage rules allow read/write');
    console.error('   3. Network connection is working');
    process.exit(1);
  }
}

testFirebaseStorage();
