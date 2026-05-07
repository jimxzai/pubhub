import { initializeApp } from "firebase/app";
import { getStorage, ref, uploadBytes, uploadString, getDownloadURL, deleteObject, listAll } from "firebase/storage";

const firebaseConfig = {
  apiKey: process.env.FIREBASE_API_KEY || "AIzaSyB0ixBMrCKHREqW36FIjsFYEp1O_l8n2kc",
  authDomain: "steelcore-eb364.firebaseapp.com",
  projectId: "steelcore-eb364",
  storageBucket: "steelcore-eb364.firebasestorage.app",
  messagingSenderId: "1023296571139",
  appId: "1:1023296571139:web:ee5f9ba8a4e5c512f68b36",
  measurementId: "G-EG2MFCJX0S"
};

const app = initializeApp(firebaseConfig);
const storage = getStorage(app);

// Upload a file (Buffer or Uint8Array)
export async function uploadFile(path, data, metadata = {}) {
  const storageRef = ref(storage, path);
  const snapshot = await uploadBytes(storageRef, data, metadata);
  return getDownloadURL(snapshot.ref);
}

// Upload text/JSON content
export async function uploadText(path, content, format = 'raw') {
  const storageRef = ref(storage, path);
  const snapshot = await uploadString(storageRef, content, format);
  return getDownloadURL(snapshot.ref);
}

// Get download URL for a file
export async function getFileUrl(path) {
  const storageRef = ref(storage, path);
  return getDownloadURL(storageRef);
}

// Delete a file
export async function deleteFile(path) {
  const storageRef = ref(storage, path);
  return deleteObject(storageRef);
}

// List all files in a directory
export async function listFiles(path) {
  const storageRef = ref(storage, path);
  const result = await listAll(storageRef);
  return {
    files: result.items.map(item => item.fullPath),
    folders: result.prefixes.map(prefix => prefix.fullPath)
  };
}

export { app, storage, ref };
