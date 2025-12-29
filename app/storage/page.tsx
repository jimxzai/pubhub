'use client';

import { useState, useEffect, useCallback } from 'react';
import { listFolder, getFileContent, deleteStorageFile, uploadStorageFile, FileItem } from '@/lib/firebase-client';

export default function StoragePage() {
  const [currentPath, setCurrentPath] = useState('');
  const [items, setItems] = useState<FileItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedFile, setSelectedFile] = useState<FileItem | null>(null);
  const [fileContent, setFileContent] = useState<string>('');
  const [uploading, setUploading] = useState(false);

  const loadFolder = useCallback(async (path: string) => {
    setLoading(true);
    try {
      const files = await listFolder(path);
      setItems(files);
    } catch (error) {
      console.error('Error loading folder:', error);
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    loadFolder(currentPath);
  }, [currentPath, loadFolder]);

  const navigateTo = (path: string) => {
    setCurrentPath(path);
    setSelectedFile(null);
    setFileContent('');
  };

  const goUp = () => {
    const parts = currentPath.split('/').filter(Boolean);
    parts.pop();
    navigateTo(parts.join('/'));
  };

  const viewFile = async (file: FileItem) => {
    setSelectedFile(file);
    if (file.name.endsWith('.md') || file.name.endsWith('.txt') || file.name.endsWith('.json')) {
      try {
        const content = await getFileContent(file.fullPath);
        setFileContent(content);
      } catch (error) {
        setFileContent('Error loading file content');
      }
    } else {
      setFileContent('');
    }
  };

  const handleDelete = async (file: FileItem) => {
    if (confirm(`Delete ${file.name}?`)) {
      try {
        await deleteStorageFile(file.fullPath);
        loadFolder(currentPath);
        setSelectedFile(null);
      } catch (error) {
        alert('Error deleting file');
      }
    }
  };

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    try {
      const path = currentPath ? `${currentPath}/${file.name}` : file.name;
      await uploadStorageFile(path, file);
      loadFolder(currentPath);
    } catch (error) {
      alert('Error uploading file');
    }
    setUploading(false);
    e.target.value = '';
  };

  const breadcrumbs = ['root', ...currentPath.split('/').filter(Boolean)];

  return (
    <main className="min-h-screen p-8 max-w-6xl mx-auto">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-primary-900 mb-2">📁 Storage Browser</h1>
        <p className="text-gray-600">Firebase Storage file manager</p>
      </header>

      {/* Breadcrumb */}
      <nav className="mb-4 flex items-center gap-2 text-sm">
        {breadcrumbs.map((crumb, i) => (
          <span key={i} className="flex items-center gap-2">
            {i > 0 && <span className="text-gray-400">/</span>}
            <button
              onClick={() => navigateTo(breadcrumbs.slice(1, i + 1).join('/'))}
              className="text-blue-600 hover:underline"
            >
              {crumb}
            </button>
          </span>
        ))}
      </nav>

      <div className="flex gap-8">
        {/* File list */}
        <div className="flex-1">
          <div className="flex items-center gap-4 mb-4">
            {currentPath && (
              <button
                onClick={goUp}
                className="px-3 py-1 text-sm bg-gray-100 rounded hover:bg-gray-200"
              >
                ⬆️ Up
              </button>
            )}
            <label className="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600 cursor-pointer">
              {uploading ? '⏳ Uploading...' : '📤 Upload'}
              <input type="file" className="hidden" onChange={handleUpload} disabled={uploading} />
            </label>
            <button
              onClick={() => loadFolder(currentPath)}
              className="px-3 py-1 text-sm bg-gray-100 rounded hover:bg-gray-200"
            >
              🔄 Refresh
            </button>
          </div>

          {loading ? (
            <div className="text-gray-500">Loading...</div>
          ) : items.length === 0 ? (
            <div className="text-gray-500">Empty folder</div>
          ) : (
            <ul className="border rounded-lg divide-y">
              {items.map((item) => (
                <li
                  key={item.fullPath}
                  className={`p-3 flex items-center gap-3 hover:bg-gray-50 cursor-pointer ${
                    selectedFile?.fullPath === item.fullPath ? 'bg-blue-50' : ''
                  }`}
                  onClick={() => (item.isFolder ? navigateTo(item.fullPath) : viewFile(item))}
                >
                  <span className="text-xl">{item.isFolder ? '📁' : '📄'}</span>
                  <span className="flex-1">{item.name}</span>
                  {!item.isFolder && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDelete(item);
                      }}
                      className="text-red-500 hover:text-red-700 text-sm"
                    >
                      🗑️
                    </button>
                  )}
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Preview panel */}
        <div className="w-1/2 border rounded-lg p-4 bg-gray-50">
          {selectedFile ? (
            <div>
              <h3 className="font-bold mb-2">{selectedFile.name}</h3>
              <p className="text-sm text-gray-500 mb-4">{selectedFile.fullPath}</p>
              {selectedFile.url && (
                <a
                  href={selectedFile.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 text-sm hover:underline block mb-4"
                >
                  🔗 Open in new tab
                </a>
              )}
              {fileContent && (
                <pre className="text-sm bg-white p-4 rounded border overflow-auto max-h-96 whitespace-pre-wrap">
                  {fileContent}
                </pre>
              )}
            </div>
          ) : (
            <div className="text-gray-400 text-center py-12">
              Select a file to preview
            </div>
          )}
        </div>
      </div>

      <footer className="mt-16 pt-8 border-t text-center text-sm text-gray-500">
        <a href="/" className="text-blue-600 hover:underline">← Back to Home</a>
      </footer>
    </main>
  );
}
