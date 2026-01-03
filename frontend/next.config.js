const removeImports = require("next-remove-imports")();
module.exports = removeImports({
  experimental: { esmExternals: true },
});

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  swcMinify: true,
  output: 'standalone',
};

const buildConfig = (_phase) => {
  const plugins = [];
  const config = plugins.reduce((acc, next) => next(acc), {
    ...nextConfig,
  });
  return config;
};

module.exports = buildConfig();
