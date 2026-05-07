import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * 投研档案库 · Quartz 配置
 *
 * 部署前请修改：
 * 1. baseUrl: 改成你的 GitHub Pages 地址
 * 2. pageTitle: 改成你想要的站点名
 * 3. 如果用自定义域名，baseUrl 改成你的域名（不带 https://）
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "投研档案库",
    pageTitleSuffix: " · Research Archive",
    enableSPA: true,
    enablePopovers: true,        // 鼠标悬停在双向链接上预览内容
    analytics: null,             // 不需要统计分析
    locale: "zh-CN",
    baseUrl: "learnerdoris.github.io/research",// 改成你的实际地址
    ignorePatterns: [
      "private",                 // private/ 文件夹下的内容不会发布
      "templates",               // 模板不发布
      ".obsidian",
      "**/*.canvas",
    ],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Source Serif Pro",   // 标题用衬线字体（FT 风格）
        body: "Inter",                 // 正文用 Inter（清晰好读）
        code: "JetBrains Mono",        // 代码字体
      },
      colors: {
        lightMode: {
          light: "#faf8f5",            // 米白底（FT 那种暖色调）
          lightgray: "#e5e5e5",
          gray: "#b8b8b8",
          darkgray: "#4e4e4e",
          dark: "#2b2b2b",
          secondary: "#284b63",        // 深蓝（链接 / 强调）
          tertiary: "#84a59d",
          highlight: "rgba(143, 159, 169, 0.15)",
          textHighlight: "#fff236",
        },
        darkMode: {
          light: "#161618",
          lightgray: "#393639",
          gray: "#646464",
          darkgray: "#d4d4d4",
          dark: "#ebebec",
          secondary: "#7b97aa",
          tertiary: "#84a59d",
          highlight: "rgba(143, 159, 169, 0.15)",
          textHighlight: "#b3aa0288",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: { light: "github-light", dark: "github-dark" },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [
      Plugin.RemoveDrafts(),         // draft: true 的不发布
    ],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.NotFoundPage(),
    ],
  },
}

export default config
