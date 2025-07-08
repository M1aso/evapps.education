import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Internationalization configuration
  i18n: {
    locales: ["en", "ru"],
    defaultLocale: "en",
  },
};

export default nextConfig;
