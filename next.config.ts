import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  // Next.js 16.1 - Turbopack is now stable with file system caching
  // Run: pnpm dev (Turbopack is default in 16.1)
  // Or: pnpm dev --inspect (for debugging)

  // Enable React strict mode
  reactStrictMode: true,

  // Typed routes (moved from experimental in 16.1)
  typedRoutes: true,

  // Experimental features for Next.js 16.1
  experimental: {
    // Optimize package imports
    optimizePackageImports: ['lucide-react'],
  },

  // Turbopack root configuration
  turbopack: {
    root: process.cwd(),
  },

  // Turbopack configuration (stable in 16.1)
  // File system caching is now ON by default
  // Transitive dependencies are automatically resolved

  // Image optimization
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.gty.org',
      },
    ],
  },

  // Headers for security
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
        ],
      },
    ]
  },

  // Redirects (if needed)
  async redirects() {
    return []
  },
}

export default nextConfig
