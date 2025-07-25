import { defineConfig } from "vitepress";

// https://vitepress.dev/reference/site-config
export default defineConfig({
  // Use Canonical URL, but only the path and with no trailing /
  // End result is like: `/en/latest`
  base: process.env.READTHEDOCS_CANONICAL_URL
    ? new URL(process.env.READTHEDOCS_CANONICAL_URL).pathname.replace(/\/$/, "")
    : "",
  title: "Qt Material UI",
  description: "Material 3 component library for Qt Widgets",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    search: {
      provider: "local",
    },
    sidebar: [
      {
        text: "Get Started",
        items: [
          {
            text: "Development Status",
            link: "/get-started/development-status",
          },
          { text: "Installation", link: "/get-started/installation" },
          { text: "Core Concepts", link: "/get-started/core-concepts" },
          { text: "Theming", link: "/get-started/theming" },
        ],
      },
      {
        text: "Components",
        items: [
          { text: "Buttons", link: "/components/buttons" },
          { text: "Checkbox", link: "/components/checkbox" },
          { text: "ComboBox", link: "/components/combobox" },
          { text: "Icons", link: "/components/icons" },
          { text: "Menu", link: "/components/menu" },
          {
            text: "Progress Indicators",
            link: "/components/progress-indicators",
          },
          { text: "Switch", link: "/components/switch" },
          { text: "Text Fields", link: "/components/text-fields" },
          { text: "Typography", link: "/components/typography" },
        ],
      },
    ],
    socialLinks: [
      { icon: "github", link: "https://github.com/herobank110/qt-material-ui" },
    ],
  },
});
