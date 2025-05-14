import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
    // Use Canonical URL, but only the path and with no trailing /
    // End result is like: `/en/latest`
    base: process.env.READTHEDOCS_CANONICAL_URL
        ? new URL(process.env.READTHEDOCS_CANONICAL_URL).pathname.replace(/\/$/, "")
        : "",
    title: "qt-material-ui",
    description: "Material 3 component library for Qt Widgets",
    themeConfig: {
        // https://vitepress.dev/reference/default-theme-config
        search: {
            provider: 'local'
        },
        sidebar: [
            {
                text: 'Components',
                items: [
                    // { text: 'Introduction', link: '/components' },
                    { text: 'Buttons', link: '/components/buttons' },
                    { text: 'Switch', link: '/components/switch' },
                ]
            }
        ],
        socialLinks: [
            { icon: 'github', link: 'https://github.com/herobank110/qt-material-ui' }
        ]
    }
})
