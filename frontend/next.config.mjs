/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['localhost', 'mycdn.com'],
  },
  async rewrites() {
    return [
      {
        source: '/api/backend/:path*',
        destination: (process.env.NEXT_PUBLIC_BACKEND || 'http://localhost:8000') + '/api/:path*',
      },
    ];
  },
};

export default nextConfig;
