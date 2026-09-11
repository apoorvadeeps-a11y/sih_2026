import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://sih-2026-jjd8.onrender.com/:path*',
      },
    ];
  },
};

export default nextConfig;