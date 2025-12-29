import { initializeApp, getApps } from 'firebase/app';
import { getStorage, ref, listAll, getDownloadURL, deleteObject, uploadBytes } from 'firebase/storage';

const firebaseConfig = {
  apiKey: "AIzaSyB0ixBMrCKHREqW36FIjsFYEp1O_l8n2kc",
  authDomain: "steelcore-eb364.firebaseapp.com",
  projectId: "steelcore-eb364",
  storageBucket: "steelcore-eb364.firebasestorage.app",
  messagingSenderId: "1023296571139",
  appId: "1:1023296571139:web:ee5f9ba8a4e5c512f68b36",
};

// Initialize Firebase only once
const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0];
const storage = getStorage(app);

export interface FileItem {
  name: string;
  fullPath: string;
  isFolder: boolean;
  size?: number;
  url?: string;
  contentType?: string;
}

export async function listFolder(path: string = ''): Promise<FileItem[]> {
  const folderRef = ref(storage, path);
  const result = await listAll(folderRef);

  const items: FileItem[] = [];

  // Add folders
  for (const prefix of result.prefixes) {
    items.push({
      name: prefix.name,
      fullPath: prefix.fullPath,
      isFolder: true,
    });
  }

  // Add files
  for (const item of result.items) {
    try {
      const url = await getDownloadURL(item);
      items.push({
        name: item.name,
        fullPath: item.fullPath,
        isFolder: false,
        url,
      });
    } catch {
      items.push({
        name: item.name,
        fullPath: item.fullPath,
        isFolder: false,
      });
    }
  }

  return items.sort((a, b) => {
    if (a.isFolder !== b.isFolder) return a.isFolder ? -1 : 1;
    return a.name.localeCompare(b.name);
  });
}

export async function getFileContent(path: string): Promise<string> {
  const fileRef = ref(storage, path);
  const url = await getDownloadURL(fileRef);
  const response = await fetch(url);
  return response.text();
}

export async function deleteStorageFile(path: string): Promise<void> {
  const fileRef = ref(storage, path);
  await deleteObject(fileRef);
}

export async function uploadStorageFile(path: string, file: File): Promise<string> {
  const fileRef = ref(storage, path);
  await uploadBytes(fileRef, file);
  return getDownloadURL(fileRef);
}

export { storage, ref };
