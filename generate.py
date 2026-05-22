#!/usr/bin/env python3
"""Generate 7 PostHog cheatsheet infographics + an index page."""

from pathlib import Path
from html import escape

OUT = Path(__file__).parent

# ---------------------------------------------------------------------------
# DATA. One entry per cheatsheet.
# ---------------------------------------------------------------------------
PAGES = {
    "ai": {
        "title": "PostHog AI",
        "subtitle": "Cheatsheet",
        "tagline": "Max + MCP as the chat/agent surface for everything PostHog.",
        "accent": "#b62ad9",
        "icon": '<svg width="100%" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill-rule="evenodd" d="M12 9c-1.356 0-2.857.857-4.284 2.9a.174.174 0 0 0 0 .2C9.143 14.142 10.644 15 12 15c1.356 0 2.857-.857 4.284-2.9l.615.428-.615-.429a.174.174 0 0 0 0-.198C14.857 9.857 13.356 9 12 9Zm0-1.5c2.043 0 3.942 1.29 5.514 3.542.401.575.401 1.341 0 1.916C15.942 15.209 14.044 16.5 12 16.5c-2.043 0-3.942-1.29-5.514-3.542a1.674 1.674 0 0 1 0-1.916C8.058 8.791 9.956 7.5 12 7.5Z" clip-rule="evenodd"/><path fill-rule="evenodd" d="M18.01 5.99A8.504 8.504 0 0 0 7.836 4.587a.75.75 0 1 1-.735-1.307c3.81-2.143 8.726-1.595 11.97 1.649 3.244 3.244 3.792 8.16 1.65 11.97a.75.75 0 1 1-1.308-.735A8.504 8.504 0 0 0 18.01 5.99ZM4.3 6.815a.75.75 0 0 1 .287 1.021 8.504 8.504 0 0 0 11.577 11.577.75.75 0 0 1 .735 1.308c-3.81 2.142-8.726 1.594-11.97-1.65-3.244-3.244-3.793-8.16-1.65-11.97a.75.75 0 0 1 1.022-.286ZM10.75 12a1.25 1.25 0 1 1 2.5 0 1.25 1.25 0 0 1-2.5 0Z" clip-rule="evenodd"/></svg>',
        "summary": "Don't use the UI! Ask the agent in the in-app sidebar, over MCP or in Slack.",
        "why": (
            "PostHog AI is the agent surface for "
            "<b>insights, queries, cohorts, flags, and dashboards</b>. "
            "In-app sidebar (Max), MCP in your coding agent, PostHog in Slack: same idea on different surfaces."
        ),
        "quote": "<strong>Don't use the UI.</strong> Ask the agent to do what you need.",
        "blocks": [
            {
                "type": "grid2",
                "title": "Where to access it",
                "items": [
                    ("In-app sidebar (Max)", "Chat assistant inside posthog.com"),
                    ("MCP server", "Claude Code, Cursor, Codex, Gemini, Claude Desktop, Windsurf, Zed, VS Code"),
                    ("Slack", "Answers questions and writes code in your team Slack"),
                    ("Skills", "Reusable instruction units agents call via MCP. Teach once, reuse everywhere."),
                ],
            },
            {
                "type": "tips",
                "title": "Tips &amp; tricks",
                "items": [
                    ("Preview HogQL before you persist.", "Run <code>query-generate-hogql-from-question</code> first, eyeball the SQL, then call <code>insight-create-from-query</code>."),
                    ("AI is the SQL finisher, not the author.", "Write SQL to ~80–90% yourself, then let Max/MCP close the gap. Best speed-to-correctness ratio."),
                    ("MCP calls are almost free, so use them in CI.", "Ask “is checkout worse than last week?” <em>before</em> you merge. Cheaper than post-deploy alerts."),
                    ("Review every tool call.", "MCP servers are prompt-injection targets. A hostile event could trick an LLM into writing flags. Default to manual approval."),
                ],
            },
            {
                "type": "patterns",
                "title": "Customer patterns in the wild",
                "items": [
                    ("🛠 AI app-builder", "multi-stack", "Engineer uses LLM analytics + experiments + flags as one stack. Spotted unequal attention allocation in a trace, rolled fix behind a flag without leaving the surface.", "Power move: A/B the observability tools themselves, not just the prompts."),
                    ("🐘 Dev-first Postgres", "10× YoY", "Consolidated 3+ analytics tools onto PostHog. Used AI for gnarly SQL their PMs couldn't write, then found AI code-gen as top acquisition channel.", "AI-generated SQL turned a PM bottleneck into a discovery channel."),
                    ("🔎 AI semantic search", "days → 1 session", "Eng lead pairs AI assistant with session replay: AI finishes the last 10–20% of SQL, replays show <em>why</em> anomalies happened.", "Analyst-to-engineer round trip collapses to one debugging session."),
                ],
            },
        ],
        "setup_label": "One-liner setup",
        "setup_command": "npx @posthog/wizard@latest mcp add",
        "setup_meta": "Works with Cursor · Claude Code · Claude Desktop · Codex · VS Code · Windsurf · Zed",
        "links": [
            "posthog.com/docs/posthog-ai",
            "posthog.com/docs/model-context-protocol",
            "posthog.com/docs/product-analytics/build-insights-mcp",
            "github.com/PostHog/mcp",
        ],
    },

    "cohorts": {
        "title": "PostHog Cohorts",
        "subtitle": "Cheatsheet",
        "tagline": "Turn “users who did X” into a reusable handle across PostHog",
        "accent": "#36c46f",
        "icon": '<svg width="100%" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M7.5 4.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5ZM3.5 7a4 4 0 1 1 8 0 4 4 0 0 1-8 0Zm13-2.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5Zm-4 2.5a4 4 0 1 1 8 0 4 4 0 0 1-8 0Zm6.692 7.268c-1.381-.87-3.024-1-4.48-.395a.75.75 0 0 1-.575-1.385 6.342 6.342 0 0 1 5.855.511c1.796 1.133 3.171 3.188 3.628 6.067.17 1.073-.698 1.934-1.693 1.934H16.75a.75.75 0 0 1 0-1.5h5.177a.23.23 0 0 0 .172-.072.145.145 0 0 0 .04-.127c-.4-2.52-1.571-4.165-2.947-5.033ZM7.429 13.5c-2.384 0-4.934 1.811-5.567 5.798a.149.149 0 0 0 .04.13.228.228 0 0 0 .171.072h10.711c.073 0 .133-.03.17-.073a.149.149 0 0 0 .041-.129c-.633-3.987-3.183-5.798-5.566-5.798Zm0-1.5c3.243 0 6.319 2.476 7.047 7.063.17 1.07-.694 1.937-1.692 1.937H2.073c-.998 0-1.862-.867-1.692-1.937C1.109 14.476 4.185 12 7.429 12Z"/></svg>',
        "summary": "Build the cohort once, then navigate by it across surveys, flags, insights, and replay.",
        "why": (
            "Cohorts turn “users who did X” into a reusable handle you can target with "
            "<b>surveys, feature flags, insights, and replay filters</b>. Stop hunting through raw user lists. "
            "Build the cohort once, then <em>navigate by it</em> across PostHog."
        ),
        "quote": "<strong>Build once, navigate by it.</strong> Chained workflows, per-segment comparisons.",
        "blocks": [
            {
                "type": "bullets",
                "title": "Honest caveats (from the team)",
                "items": [
                    "<b>No survey-answer filter yet.</b> Use survey branching for answer-level routing.",
                    "<b>Autocapture cohorts at scale = labor-intensive.</b> Works for early-stage; refresh tax grows.",
                    "<b>Cohort path is buried in some views.</b> Replay frustration-signals filter takes ~4 clicks.",
                ],
            },
            {
                "type": "tips",
                "title": "Tips &amp; tricks",
                "items": [
                    ("Pin cohorts to your sidebar.", "Multiple customers got lost mid-workflow. The sidebar is customizable, but almost nobody discovers this. Cheap win."),
                    ("Cohort drill-down as navigation, not analysis.", "Replay path: dashboard → funnel → cohort → recording. Build the funnel, materialize the failing cohort, drill in."),
                    ("Survey respondents → cohort → follow-up.", "Cohort survey takers, then target with a deeper second survey or interview booking. Surveys become a research-recruitment funnel."),
                    ("Autocapture actions as cohort seeds.", "Pre-instrumentation products can still build behavioral cohorts: autocapture → action → cohort. Unblocks early-stage teams."),
                    ("Geographic cohorts for multi-market redesigns.", "US vs. UK cohorts on replay frustration signals give per-market before/after for any rollout."),
                ],
            },
            {
                "type": "patterns",
                "title": "Customer patterns in the wild",
                "items": [
                    ("🎓 EdTech startup (~900 users)", "~50% response", "PM wanted to survey only students who used the AI tutor “enough.” Built a weekly autocapture → static cohort → re-target loop. Painful but worked.", "Cohorts unlock behavioral targeting even without instrumented events, if you can stomach the refresh tax."),
                    ("🏢 B2B SaaS (1.5M MAU)", "replaced Pendo", "Growth PM migrated all surveys to PostHog: satisfaction survey → respondents become a cohort → that cohort gets an interview-booking survey.", "Cohorts + surveys = automated user research recruitment, no standalone tooling."),
                    ("🌍 Multi-country SaaS", "phased rollout", "PM built US and UK cohorts, applied them to replay frustration signals during a beta. Clean before/after view per market, used to gate the wider rollout.", "Cohorts as a per-market product-quality lens during a phased rollout."),
                ],
            },
        ],
        "setup_label": "Canonical entry",
        "setup_command": "posthog.com/docs/data/cohorts",
        "setup_meta": "Covers static vs. dynamic, behavioral cohorts with event-count + time-window conditions",
        "links": [
            "posthog.com/docs/data/cohorts",
            "posthog.com/docs/surveys",
            "posthog.com/docs/feature-flags",
            "posthog.com/docs/session-replay",
        ],
    },

    "experiments": {
        "title": "PostHog Experiments",
        "subtitle": "Cheatsheet",
        "tagline": "Causal impact, inside the same tool as your events, flags, and replays",
        "accent": "#a78bfa",
        "icon": '<svg width="100%" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M7 6.75A.75.75 0 0 1 7.75 6h8.5a.75.75 0 0 1 0 1.5H16v3.233a31.851 31.851 0 0 0 .885 1.006c.322.358.665.738.995 1.132.72.86 1.434 1.842 1.83 2.948.18.505.29 1.04.29 1.597A4.584 4.584 0 0 1 15.416 22H8.584A4.584 4.584 0 0 1 4 17.416c0-.558.11-1.092.29-1.597.396-1.106 1.11-2.089 1.83-2.948.33-.394.673-.774.995-1.132l.093-.104c.287-.317.553-.616.792-.902V7.5h-.25A.75.75 0 0 1 7 6.75Zm2.5.75v3.763l-.164.206c-.31.386-.662.78-1.013 1.17l-.091.101c-.325.361-.65.722-.962 1.095-.345.41-.66.82-.928 1.234l.098-.015c.895-.137 2.053-.275 2.99-.25 1.137.03 2 .302 2.774.545l.021.007c.779.245 1.469.46 2.384.484.797.02 1.846-.1 2.725-.234.211-.032.41-.065.59-.095-.313-.566-.728-1.12-1.194-1.676-.312-.373-.637-.734-.962-1.095l-.091-.101c-.351-.39-.703-.784-1.013-1.17l-.164-.206V7.5h-5Z"/><path d="M11 4a1 1 0 1 1-2 0 1 1 0 0 1 2 0Zm4-1.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0Z"/></svg>',
        "summary": "Ship behind a flag → watch the funnel → drill into replay → decide. The loop, not the first test.",
        "why": (
            "Test causal impact, all inside the same tool as your <b>events, flags, replays, and LLM traces</b>. "
            "The real payoff isn't the first A/B; it's the loop: ship behind a flag → watch the funnel → "
            "drill into replay → decide."
        ),
        "quote": "For AI products: <strong>“the change got worse”</strong> doesn't show up as a crash.",
        "blocks": [
            {
                "type": "chips",
                "title": "Test types you can run",
                "items": [
                    ("A/A", "sanity-check setup"),
                    ("A/B/n", ">2 variants"),
                    ("Holdout", "long-term combined effect"),
                    ("Redirect", "split traffic between URLs"),
                    ("Fake door", "measure demand pre-build"),
                    ("New-user", "first-time users only"),
                    ("LLM A/B", "prompts, models, agents"),
                ],
            },
            {
                "type": "tips",
                "title": "Tips &amp; tricks",
                "items": [
                    ("Bootstrap flags on the server, not the client.", "Browser fetch = flash of control variant + ad-blocker holes. Pass the flag with the page render."),
                    ("Run an A/A test first.", "Both variants identical. A persistent gap signals a setup bug: events dropped, users bouncing between variants, bad split."),
                    ("Filter ineligible users <em>before</em> the flag check.", "Otherwise everyone hitting that code path gets an exposure, lift gets diluted by zero-effect users."),
                    ("Don't act before you hit sample size.", "Looking is fine. Acting on early numbers isn't. Watch win prob &amp; effect size over time, not today."),
                    ("Test the experiment itself with 5–10% first.", "If the variant is broken at 50% rollout, users are contaminated, and you can't restart cleanly."),
                ],
            },
            {
                "type": "patterns",
                "title": "Customer patterns in the wild",
                "items": [
                    ("🤝 Co-founder matching", "+40% messages", "4-variant test hiding stale profiles at 3/6/9/12 weeks; 6-week won (+35% match acceptance). Same team killed a feature when basically nobody used the minimal version.", "Experiments aren't just for picking winners. They're for picking <em>how aggressive</em>, and killing without sunk-cost guilt."),
                    ("⚖️ AI model comparison", "19× volume", "Anonymous-LLM voting product. Every UI change risks skewing rankings, so they experiment on everything: button placement, swipe redesigns, AI routers. Event volume 19× in 6 months without ranking drift.", "Experiments aren't just about lift. They're about not silently breaking the dataset you depend on."),
                    ("⚙️ AI app-building platform", "flags + exp + LLM", "Flags for gradual rollouts, experiments for new ideas, traces for oddness. When GPT-5 shipped weird, they didn't guess. They inspected traces and found attention-distribution changes.", "“The change got worse” doesn't show up as a crash; you need trace-level data to even notice."),
                ],
            },
        ],
        "setup_label": "Start here",
        "setup_command": "posthog.com/docs/experiments/start-here",
        "setup_meta": "Per-framework tutorials: Next.js · Django · Rails · iOS · LLM A/B",
        "links": [
            "posthog.com/docs/experiments/start-here",
            "posthog.com/docs/experiments/best-practices",
            "posthog.com/docs/experiments/tracking-long-term-metrics",
            "posthog.com/docs/experiments/data-warehouse",
        ],
    },

    "feature-flags": {
        "title": "PostHog Feature Flags",
        "subtitle": "Cheatsheet",
        "tagline": "Decouple deploy from release. Ship disabled, flip slowly, watch.",
        "accent": "#30abc6",
        "icon": '<svg width="100%" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M1.5 11.75A5.75 5.75 0 0 1 7.25 6h10.5a5.75 5.75 0 0 1 5.75 5.75v.5A5.75 5.75 0 0 1 17.75 18H7.25a5.75 5.75 0 0 1-5.75-5.75v-.5Zm16-4.25a4.5 4.5 0 1 0 0 9 4.5 4.5 0 0 0 0-9Z"/></svg>',
        "summary": "Flag every release, filter replays by the flag, and watch the first 20–50 sessions before going wider.",
        "why": (
            "Feature flags decouple <b>deploy</b> from <b>release</b>. Ship disabled, flip for a small %, watch, widen. "
            "The strongest customer pattern: flag every release, filter replays by that flag, watch the first 20–50 "
            "real sessions before going wider."
        ),
        "quote": "<strong>Flag everything.</strong> Low cost, free optionality downstream.",
        "blocks": [
            {
                "type": "tips",
                "title": "Tips &amp; tricks",
                "items": [
                    ("Flag-filtered replay = your deployment monitor.", "Flip for a small %, open Replay filtered by the flag, watch 20–50 sessions. Faster than alerting; shows behavior, not error counts. <em>3+ teams in research.</em>"),
                    ("Flag everything by default.", "“We try to feature flag everything we are releasing.” Kill switches, gradual rollouts, A/B, rollbacks all become free downstream."),
                    ("Flags are runtime UX config, not just code branches.", "One AI team drives a “we're seeing issues” banner via a flag toggled by an error-monitor webhook. Wire toggles to <em>ops signals</em>, not humans."),
                    ("History tab is your audit log.", "Growth team uses it as primary “what changed and when?” when investigating data anomalies, especially valuable when AI agents have flag access."),
                    ("Use flag conditions for survey targeting.", "Skip weekly manual cohort refreshes. Flag conditions in survey targeting solve the same problem with no maintenance loop."),
                ],
            },
            {
                "type": "patterns",
                "title": "Customer patterns in the wild",
                "items": [
                    ("⚡ Solo-dev AI startup", "automated honesty", "Wired error-monitor webhook to a flag controlling an in-product status banner. OOM errors → banner flips automatically → users see “we're experiencing issues.” No human in loop.", "Flags closed the gap between “infra knows” and “users know.”"),
                    ("🏗 B2B infra (~30 eng)", "flag-rollout + replay", "Every feature ships behind a flag. As soon as it's live, they filter recordings by that flag and watch employees use it in-office before widening to customers.", "Caught issues pre-customer-rollout without writing any custom monitoring."),
                    ("🛒 Mid-market ecom (ex-Heap)", "one workflow", "Director of eng listed flags + experiments as explicit pull factors (Heap had neither). First A/B test on a “Shop Now” redesign, used flag-filtered replay to understand <em>why</em>.", "Flags + experiments + replay aren't three tools. They're one workflow."),
                ],
            },
        ],
        "setup_label": "Canonical entry",
        "setup_command": "posthog.com/docs/feature-flags",
        "setup_meta": "Creating flags · Rolling out · Multivariate · Local evaluation · Flags + Experiments",
        "links": [
            "posthog.com/docs/feature-flags",
            "posthog.com/docs/feature-flags/local-evaluation",
            "posthog.com/docs/experiments",
            "posthog.com/docs/session-replay",
        ],
    },

    "funnels": {
        "title": "PostHog Funnels",
        "subtitle": "Cheatsheet",
        "tagline": "Connective tissue between every other PostHog product",
        "accent": "#2f80fa",
        "icon": '<svg width="100%" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M3 5a1 1 0 0 1 1-1h16a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V5ZM3 11a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-2ZM3 17a1 1 0 0 1 1-1h3a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-2Z"/></svg>',
        "summary": "Build the funnel, click the drop-off step, and jump straight into the replays of users who didn't convert.",
        "why": (
            "Funnels are the <b>connective tissue</b> between every other PostHog product. "
            "Build a funnel for a key flow, click the drop-off step, jump straight into the replays "
            "of users who didn't convert."
        ),
        "quote": "Funnels tell you <strong>that</strong> something changed. Replay tells you <strong>why</strong>.",
        "blocks": [
            {
                "type": "tips",
                "title": "Tips &amp; tricks",
                "items": [
                    ("Funnel = entry point into Replay, not the replay list.", "Strongest pattern across 5+ customers. Funnel acts as a selection filter, since the raw replay feed is too noisy past a few hundred sessions/day."),
                    ("Break funnels down by something you don't have a hypothesis for.", "One PM found her product had two different customer verticals only after breaking down trial→paid. Don't just slice by browser/country."),
                    ("Validate UI changes with a funnel <em>before</em> you A/B test.", "Cheap pre-experiment validation, much faster than waiting for a test to power. Saved one team from rolling a regressive age-verification step."),
                    ("Funnel position is a prioritization primitive.", "Errors on a funnel step matter ~10× more than errors elsewhere. Same logic for alerts, surveys, NPS prompts. Reuse via funnel-actor cohorts."),
                    ("Tune the mechanics. Three settings first-timers leave default.", "<b>Strict vs. unordered</b> · <b>Conversion window</b> (set to your real cycle, not 14 days) · <b>Exclusion steps</b> to filter exit paths."),
                ],
            },
            {
                "type": "patterns",
                "title": "Customer patterns in the wild",
                "items": [
                    ("🎨 AI creative-tools PM", "2 hidden audiences", "Built trial→paid funnel as her main dashboard. Breaking it down revealed her product had two different verticals (B2C creators vs. event organizers) converting at very different rates.", "Funnel as discovery tool, not just a KPI."),
                    ("🇪🇺 EdTech (interview prep)", "daily ritual", "Engineers run a daily replay-watching ritual scoped to four named flows. One funnel per flow → click highest drop-off → watch failed sessions. Shipped dozens of small UI fixes from this loop.", "A daily funnel-driven replay ritual finds friction no monitoring tool would alert on."),
                    ("🎓 Education non-profit", "saved weeks", "Suspected an age-verification step would tank conversion. Shipped to a slice → watched the funnel → saw the drop → replays showed where users got confused → redesigned before wide rollout.", "Funnel + replay loop is the cheapest insurance against shipping bad UX."),
                ],
            },
        ],
        "setup_label": "Canonical entry",
        "setup_command": "posthog.com/docs/product-analytics/funnels",
        "setup_meta": "Plus data-warehouse insights for fancy funnels with Stripe / Postgres data",
        "links": [
            "posthog.com/docs/product-analytics/funnels",
            "posthog.com/docs/data-warehouse/insights",
            "posthog.com/docs/session-replay",
            "posthog.com/docs/experiments",
        ],
    },

    "heatmaps": {
        "title": "PostHog Heatmaps",
        "subtitle": "Cheatsheet",
        "tagline": "Free, near-zero perf cost for clicks, scrolls, and movement, all next to your analytics.",
        "accent": "#f7a501",
        "icon": '<svg width="100%" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M6.5 9a.5.5 0 1 1 0-1 .5.5 0 0 1 0 1ZM10 9a.5.5 0 1 1 0-1 .5.5 0 0 1 0 1Zm3.5 0a.5.5 0 1 1 0-1 .5.5 0 0 1 0 1Z"/><path fill-rule="evenodd" clip-rule="evenodd" d="M6.5 9.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm3.5 0a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm3.5 0a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm-7-.5a.5.5 0 1 1 0-1 .5.5 0 0 1 0 1ZM10 9a.5.5 0 1 1 0-1 .5.5 0 0 1 0 1Zm3-.5a.5.5 0 1 0 1 0 .5.5 0 0 0-1 0Z"/><path fill-rule="evenodd" clip-rule="evenodd" d="M2 5.75C2 4.784 2.784 4 3.75 4h16.5c.966 0 1.75.784 1.75 1.75v6.5a.75.75 0 0 1-1.5 0v-6.5a.25.25 0 0 0-.25-.25H3.75a.25.25 0 0 0-.25.25v13.5c0 .138.112.25.25.25h8.5a.75.75 0 0 1 0 1.5h-8.5A1.75 1.75 0 0 1 2 19.25V5.75Zm11.47 7.72a.75.75 0 0 1 .75-.187l7 2.154a.75.75 0 0 1 .115 1.388l-3.007 1.503-1.503 3.007a.75.75 0 0 1-1.388-.114l-2.154-7a.75.75 0 0 1 .187-.751Zm1.663 1.663 1.187 3.857.778-1.556a.75.75 0 0 1 .336-.336l1.556-.778-3.856-1.187Z"/></svg>',
        "summary": "Three views, not one. Heatmap → Clickmap → Scrollmap, on the same page in sequence.",
        "why": (
            "Free, near-zero perf cost click/scroll/movement overlays. Data piggybacks on autocapture events you "
            "already capture, with <b>no separate SDK, no consent banner, no billing line</b>. The differentiator: "
            "heatmap data lives next to your analytics, so you can pivot from click cluster → funnel → replay → experiment."
        ),
        "quote": "Most common mistake: open the Heatmap and stop. <strong>Open all three views.</strong>",
        "blocks": [
            {
                "type": "grid3",
                "title": "Three views, not one",
                "items": [
                    ("Heatmap", "Position-based", "Clicks/movements by pixel. Clicks don't need a clickable element. See where users <em>tried</em> to click on dead pixels. <b>Open for discovery.</b>"),
                    ("Clickmap", "Element-based", "Autocapture badge on each clickable element with total + rage-click counts. Resilient to layout shifts. <b>Open for direct comparison.</b>"),
                    ("Scrollmap", "Depth gradient", "Requires <code>$pageleave</code> events. Is the hero CTA above the fold? Does anyone reach the FAQ? <b>Open for reach.</b>"),
                ],
            },
            {
                "type": "tips",
                "title": "Tips &amp; tricks",
                "items": [
                    ("Use the Toolbar, not the in-app Heatmaps scene.", "Toolbar overlays heatmaps on the live site. Works on auth-gated pages, catches ~10× more issues, lets you create actions from elements without leaving the page."),
                    ("Pair heatmaps with rage-click-filtered Replays.", "<code>$rageclick</code> + <code>feature_flag = new-checkout</code> = debugging a release in two clicks. Jump from Replay timestamp straight to the aggregate heatmap."),
                    ("Wildcard URLs for templated pages.", "<code>/products/*</code>, <code>/posts/*</code>, <code>/users/:id</code>. Difference between “12 clicks, meaningless” and “12,000 clicks, here's what actually happens.”"),
                    ("Scroll depth is a property on every pageview.", "Use <code>$prev_pageview_max_scroll_percentage</code> as a filter/metric anywhere: funnels, experiments. “Reached 80% before clicking CTA.”"),
                    ("Autocapture clicks ARE the quantitative heatmap signal.", "Query click counts in HogQL, use them as experiment goals, hand them to an agent via MCP. Same data, three surfaces."),
                ],
            },
            {
                "type": "patterns",
                "title": "Customer patterns + bonus",
                "items": [
                    ("🌐 Webshare", "4–5% lifts", "Collapsed Mixpanel + Hotjar + FullStory into PostHog. ~20 experiments at any moment; small UI tweaks drive lifts they wouldn't have spotted without heatmap → replay → experiment pointing at the same place.", "It's not the heatmap alone. It's the heatmap as the trigger for the experiment."),
                    ("✍️ Grantable", "“pull more in”", "AI grant-writing tool replaced Microsoft Clarity with PostHog Heatmaps as part of a consolidation stack (also replaced Sentry, Intercom, Zapier-flavored workflows).", "Cheapest way to “buy” heatmaps is to use the one shipping next to your analytics."),
                    ("🤖 Bot detection bonus", "(0, 0) clusters", "Some teams use heatmap click data to flag automated traffic that user-agent strings miss, like scripts hammering coordinate <code>(0, 0)</code> to defeat idle timers. Filter them, every insight downstream gets cleaner.", "Heatmaps as a data-quality tool, not just UX."),
                ],
            },
        ],
        "setup_label": "Start here",
        "setup_command": "posthog.com/docs/toolbar/heatmaps",
        "setup_meta": "Toolbar docs · Scroll-depth tutorial · React walkthrough · Webshare / Kilo Code / Grantable case studies",
        "links": [
            "posthog.com/docs/toolbar/heatmaps",
            "posthog.com/docs/toolbar",
            "posthog.com/tutorials/scroll-depth",
            "posthog.com/customers/webshare",
        ],
    },

    "session-replay": {
        "title": "PostHog Session Replay",
        "subtitle": "Cheatsheet",
        "tagline": "A re-rendered DOM of what the user actually saw and did, not a video.",
        "accent": "#f35454",
        "icon": '<svg width="100%" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M13 .857a.863.863 0 0 0-.46-.776.758.758 0 0 0-.852.118l-2.4 2.143A.883.883 0 0 0 9 3c0 .254.105.496.288.658l2.4 2.143c.238.213.57.26.851.118A.863.863 0 0 0 13 5.143V4.062A8.001 8.001 0 0 1 12 20 8 8 0 0 1 5.777 6.972a1 1 0 0 0-1.554-1.258A9.962 9.962 0 0 0 2 12c0 5.523 4.477 10 10 10s10-4.477 10-10c0-5.185-3.947-9.449-9-9.95V.856ZM9 8.703c0-.547.611-.884 1.09-.6l5.564 3.297a.693.693 0 0 1 0 1.2l-5.565 3.297c-.478.284-1.089-.053-1.089-.6V8.703Z"/></svg>',
        "summary": "Don't start in the chronological list. Drill into Replay from a signal, like a funnel drop, an error, an experiment.",
        "why": (
            "Session Replay is a <b>re-rendered DOM</b> (not a video) of what the user actually saw and did. "
            "The strongest pattern is using it as the <em>“why”</em> after some other signal flagged a <em>“what”</em>, like "
            "a funnel drop, an error, an experiment arm, an anomalous session duration."
        ),
        "quote": "It also doubles as a <strong>“what's weird right now”</strong> radar for abuse, fraud, even inbound-sales signals.",
        "blocks": [
            {
                "type": "tips",
                "title": "Tips &amp; tricks",
                "items": [
                    ("Replay is a DOM, not a video.", "Open the browser inspector mid-playback. Elements respond to clicks and hovers. Grab selectors and text without rewatching."),
                    ("Don't start in the chronological list.", "All strong workflows <em>enter</em> Replay from a signal. As one PM put it: “it always seems backwards to go to the chronological list first.”"),
                    ("Saved filters are the underrated power feature.", "Heavy users said they didn't discover saved filters/collections for months. Difference between “scrolling forever” and “10 sessions worth watching this morning.”"),
                    ("Pair Replay with Error Tracking on-call.", "Backend exception → matching replay → see the UI state. One on-call eng found a stale-sidebar bug invisible in logs alone."),
                    ("Use PostHog AI for hypothesis-driven group analysis.", "Ask “users who clicked X and ran into issues” rather than “summarize this session.” That's how the most mature Replay users work."),
                    ("Replay catches things you weren't looking for.", "Real-time abuse, fraud signals, inbound-sales discovery. Multiple customers use it as a <em>“what's weird right now”</em> radar, not just retro analysis."),
                ],
            },
            {
                "type": "patterns",
                "title": "Customer patterns + bonus",
                "items": [
                    ("🎵 Solo SaaS founder", "10,000-store deal", "Watches Replay daily as a fraud + inbound-sales radar. Midnight activity spike → opened the replay expecting abuse → found someone bulk-generating commercial music. Cross-referenced the email, started a sales conversation.", "For the right product, Replay isn't retro debugging. It's a real-time business signal."),
                    ("🚨 EdTech on-call", "exception → root cause", "Top-15 Replay user at Series B edtech. Backend error fires → opens matching replay → sees the UI state. Found a stale-sidebar bug letting users “request help” on deleted content, all invisible in logs alone.", "The bridge from exception to root cause is the killer on-call workflow."),
                    ("☕ Berlin AI startup", "watch parties", "11-person team browses recordings together weekly, partly targeted, partly “morning coffee” mode. Disproved an internal assumption: users gave 2–3 min of thoughtful answers to open-ended quiz prompts.", "Watch parties turn Replay into a team ritual that surfaces qualitative truths dashboards can't."),
                ],
            },
            {
                "type": "callout",
                "title": "Bonus: Replay as evidence",
                "body": "Some customers use Replay outside analytics entirely, as evidence in legal/fraud cases, and as <em>“you did do that”</em> proof in support tickets and disputes. Not glamorous, but load-bearing for some teams.",
            },
        ],
        "setup_label": "Start here",
        "setup_command": "posthog.com/docs/session-replay/tutorials",
        "setup_meta": "Filtering recordings walkthrough · Session Replay product page · AI summaries",
        "links": [
            "posthog.com/docs/session-replay/tutorials",
            "posthog.com/session-replay",
            "posthog.com/tutorials/filter-session-recordings",
            "posthog.com/docs/error-tracking",
        ],
    },
}

# ---------------------------------------------------------------------------
# Shared CSS. The accent color is injected per page via a CSS variable.
# ---------------------------------------------------------------------------
BASE_CSS = """
@page { size: letter; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  background: #f4f1ea;
  color: #1d1f27;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
.page {
  width: 8.5in;
  margin: 0 auto;
  padding: 0.35in 0.4in;
  background: #f4f1ea;
  display: grid;
  grid-template-rows: auto auto 1fr auto;
  gap: 10px;
}
header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 18px; background: #1d1f27; color: #fff; border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}
.ph-logo-header { height: 28px; width: auto; }
.ph-logo-bottom {
  height: 28px; width: auto;
  display: block; margin: 12px auto 0;
  opacity: 0.6;
}
.brand { display: flex; align-items: center; gap: 12px; }
.logo {
  width: 38px; height: 38px; background: var(--accent); border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; color: #fff; font-size: 18px;
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 25%, transparent);
  flex-shrink: 0;
}
.logo svg { width: 22px; height: 22px; display: block; }
h1 { font-size: 22px; letter-spacing: -0.5px; }
.tagline { color: #f4f1ea; font-size: 11px; opacity: 0.75; }
.pill {
  background: var(--accent); color: #fff;
  padding: 6px 12px; border-radius: 999px;
  font-size: 11px; font-weight: 700; letter-spacing: 0.5px;
  text-transform: uppercase;
}
.hero {
  background: #fff; border: 2px solid #1d1f27; border-radius: 10px;
  padding: 12px 16px;
  display: grid; grid-template-columns: 2fr 1fr; gap: 14px; align-items: center;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}
.hero h2 {
  font-size: 13px; text-transform: uppercase; letter-spacing: 1px;
  color: #1d1f27; margin-bottom: 4px;
}
.hero p { font-size: 11.5px; line-height: 1.4; color: #333; }
.hero strong { background: #ffe066; padding: 1px 4px; border-radius: 3px; }
.quote {
  background: #f4f1ea; color: #1d1f27; padding: 10px 12px; border-radius: 8px;
  font-size: 11px; line-height: 1.4; border-left: 4px solid var(--accent);
}
.main {
  display: flex; flex-direction: column; gap: 10px;
  min-height: 0;
}
.row {
  display: flex; gap: 10px;
  min-height: 0;
}
.row > .card, .row > .callout { flex: 1 1 0; min-width: 0; }
.card {
  background: #fff; border-radius: 10px; padding: 11px 14px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
  display: flex; flex-direction: column;
}
.card h3 {
  font-size: 12.5px; text-transform: uppercase; letter-spacing: 0.8px;
  color: #1d1f27; margin-bottom: 8px;
  display: flex; align-items: center; gap: 8px;
  flex-shrink: 0;
}
.card h3 .num {
  background: var(--accent); color: #fff;
  width: 22px; height: 22px; border-radius: 6px;
  display: inline-flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 800;
}
.card-body { flex: 1; display: flex; flex-direction: column; }

/* grid2 */
.surfaces { display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; flex: 1; }
.surface { background: #f4f1ea; border-radius: 6px; padding: 7px 9px; font-size: 10.5px; line-height: 1.35; }
.surface b { color: #1d1f27; display: block; font-size: 11px; margin-bottom: 1px; }

/* grid3 */
.threeview { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; flex: 1; }
.view { background: #f4f1ea; border-radius: 6px; padding: 8px 9px; font-size: 10px; line-height: 1.35; border-top: 3px solid var(--accent); display: flex; flex-direction: column; }
.view b.head { color: #1d1f27; font-size: 11.5px; display: block; }
.view .sub { color: var(--accent); font-size: 9.5px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; display: block; font-weight: 700; }

/* chips */
.chips { display: flex; flex-wrap: wrap; gap: 6px; flex: 1; align-content: flex-start; }
.chip {
  background: #f4f1ea; border-left: 3px solid var(--accent);
  padding: 5px 9px; border-radius: 6px; font-size: 10.5px;
}
.chip b { color: #1d1f27; margin-right: 4px; }
.chip span { color: #666; font-style: italic; font-size: 9.5px; }

/* tips */
.tips { display: grid; gap: 6px; flex: 1; align-content: space-between; }
.tips.wide { grid-template-columns: 1fr 1fr; column-gap: 14px; }
.tip {
  display: grid; grid-template-columns: 22px 1fr; gap: 8px;
  font-size: 10.5px; line-height: 1.4;
  align-items: start;
}
.tip .tnum {
  background: #1d1f27; color: #f4f1ea; border-radius: 50%;
  width: 22px; height: 22px;
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; font-size: 11px; flex-shrink: 0;
}
.tip b { color: #1d1f27; }

/* bullets */
.bullets { display: grid; gap: 5px; align-content: space-between; }
.bullet {
  background: #f4f1ea; border-radius: 6px; padding: 6px 10px;
  font-size: 10.5px; line-height: 1.4; border-left: 3px solid var(--accent);
}

/* patterns */
.pattern-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; flex: 1; }
.pattern {
  background: #f4f1ea; border-radius: 6px;
  padding: 8px 10px; font-size: 10px; line-height: 1.4;
  display: flex; flex-direction: column;
}
.pattern h4 { font-size: 11px; color: #1d1f27; margin-bottom: 4px; }
.pattern .body { flex: 1; }
.pattern .punch {
  margin-top: 5px; padding-top: 5px;
  border-top: 1px dashed #c9c4b7;
  font-style: italic; color: #1d1f27; font-weight: 600;
}
.stat {
  display: inline-block; background: var(--accent); color: #fff;
  padding: 1px 6px; border-radius: 4px; font-weight: 700; font-size: 9.5px;
  align-self: flex-start;
  margin-bottom: 4px;
}

/* callout */
.callout {
  background: #1d1f27; color: #f4f1ea; border-radius: 8px;
  padding: 10px 14px; font-size: 10.5px; line-height: 1.45;
  border-left: 4px solid var(--accent);
}
.callout b { color: var(--accent); display: block; font-size: 11px;
  text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 4px; }
.callout em { color: #fff; }

/* code */
code {
  font-family: "SF Mono", Menlo, Consolas, monospace;
  background: color-mix(in srgb, var(--accent) 15%, white);
  color: #1d1f27;
  padding: 1px 5px; border-radius: 3px; font-size: 10px;
}

/* footer */
footer {
  background: #1d1f27; color: #fff; border-radius: 10px;
  padding: 10px 16px;
  display: grid; grid-template-columns: auto 1fr; gap: 14px; align-items: center;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}
.setup { font-size: 10px; color: #f4f1ea; opacity: 0.85; }
.setup b { color: #f4f1ea; display: block; font-size: 10px;
  text-transform: uppercase; letter-spacing: 1px; margin-bottom: 3px; }
.setup-cmd {
  font-family: "SF Mono", Menlo, Consolas, monospace;
  background: var(--accent); color: #fff;
  padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: 600;
  display: inline-block; text-decoration: none;
}
a.setup-cmd:hover { filter: brightness(1.1); }
.setup-meta { margin-top: 4px; font-size: 9px; opacity: 0.7; }
.links {
  display: flex; flex-direction: column; align-items: flex-end;
  gap: 4px; font-size: 9.5px;
}
.footer-right {
  display: flex; flex-direction: column; align-items: flex-end;
  gap: 8px;
}
.links a { color: #f4f1ea; text-decoration: none; opacity: 0.8; }
.links a::before { content: "\\2192  "; color: var(--accent); }

@media print {
  .page {
    min-height: 11in;
    height: 11in;
    gap: 0;
    /* Move the 1fr (expanding) row from `main` to the logo row so the
       variable vertical space sits between the footer and the logo. */
    grid-template-rows: auto auto auto auto 1fr;
  }
  .page > header,
  .page > .hero,
  .page > .main {
    margin-bottom: 10px;
  }
  /* The expanding 5th row creates the gap between footer and logo */
  .ph-logo-bottom {
    align-self: end;
    margin-top: 0;
  }
}
"""

# ---------------------------------------------------------------------------
# Block renderers
# ---------------------------------------------------------------------------
def render_grid2(block, idx, wide=False):
    items_html = "".join(
        f'<div class="surface"><b>{h}</b>{b}</div>' for h, b in block["items"]
    )
    return f"""
    <div class="card">
      <h3><span class="num">{idx}</span> {block["title"]}</h3>
      <div class="card-body"><div class="surfaces">{items_html}</div></div>
    </div>
    """

def render_grid3(block, idx, wide=False):
    items_html = "".join(
        f'<div class="view"><b class="head">{h}</b><span class="sub">{s}</span>{b}</div>'
        for h, s, b in block["items"]
    )
    return f"""
    <div class="card">
      <h3><span class="num">{idx}</span> {block["title"]}</h3>
      <div class="card-body"><div class="threeview">{items_html}</div></div>
    </div>
    """

def render_chips(block, idx, wide=False):
    items_html = "".join(
        f'<div class="chip"><b>{h}</b><span>{b}</span></div>' for h, b in block["items"]
    )
    return f"""
    <div class="card">
      <h3><span class="num">{idx}</span> {block["title"]}</h3>
      <div class="card-body"><div class="chips">{items_html}</div></div>
    </div>
    """

def render_tips(block, idx, wide=False):
    items_html = "".join(
        f'<div class="tip"><div class="tnum">{i+1}</div><div><b>{h}</b> {b}</div></div>'
        for i, (h, b) in enumerate(block["items"])
    )
    wide_cls = " wide" if wide else ""
    return f"""
    <div class="card">
      <h3><span class="num">{idx}</span> {block["title"]}</h3>
      <div class="card-body"><div class="tips{wide_cls}">{items_html}</div></div>
    </div>
    """

def render_bullets(block, idx, wide=False):
    items_html = "".join(f'<div class="bullet">{i}</div>' for i in block["items"])
    return f"""
    <div class="card">
      <h3><span class="num">{idx}</span> {block["title"]}</h3>
      <div class="card-body"><div class="bullets">{items_html}</div></div>
    </div>
    """

def render_patterns(block, idx, wide=False):
    items_html = "".join(
        f'<div class="pattern"><h4>{h}</h4><span class="stat">{stat}</span><div class="body">{body}</div><div class="punch">{punch}</div></div>'
        for h, stat, body, punch in block["items"]
    )
    return f"""
    <div class="card">
      <h3><span class="num">{idx}</span> {block["title"]}</h3>
      <div class="card-body"><div class="pattern-grid">{items_html}</div></div>
    </div>
    """

def render_callout(block, idx, wide=False):
    return f"""
    <div class="callout">
      <b>{block["title"]}</b>
      {block["body"]}
    </div>
    """

RENDERERS = {
    "grid2": render_grid2,
    "grid3": render_grid3,
    "chips": render_chips,
    "tips": render_tips,
    "bullets": render_bullets,
    "patterns": render_patterns,
    "callout": render_callout,
}

# Block types that always want their own row (full-width)
ALWAYS_FULL = {"grid3", "patterns", "callout"}
# Block types that pair nicely with a tips block beside them
PAIRABLE_WITH_TIPS = {"grid2", "bullets", "chips"}

def lay_out_blocks(blocks):
    """Group blocks into rows.

    Returns a list of rows; each row is a list of (block, wide_flag) tuples.
    wide_flag tells the renderer whether the block is alone in its row.
    """
    rows = []
    i = 0
    while i < len(blocks):
        b = blocks[i]
        nxt = blocks[i + 1] if i + 1 < len(blocks) else None
        # Pair a small block with the following tips block
        if (
            b["type"] in PAIRABLE_WITH_TIPS
            and nxt is not None
            and nxt["type"] == "tips"
        ):
            rows.append([(b, False), (nxt, False)])
            i += 2
        else:
            rows.append([(b, True)])
            i += 1
    return rows

# ---------------------------------------------------------------------------
# Page renderer
# ---------------------------------------------------------------------------
URL_PREFIXES = ("posthog.com", "github.com", "docs.", "www.")

def is_url(s):
    return s.startswith("http") or s.startswith(URL_PREFIXES)

def href_for(s):
    return s if s.startswith("http") else f"https://{s}"

def render_page(slug, data):
    short_title = data["title"].removeprefix("PostHog ").strip()
    rows = lay_out_blocks(data["blocks"])
    # Renumber blocks for the heading badges in display order
    block_index = 0
    rows_html_parts = []
    for row in rows:
        cards_html = []
        for block, wide in row:
            block_index += 1
            cards_html.append(RENDERERS[block["type"]](block, block_index, wide=wide))
        rows_html_parts.append(f'<div class="row">{"".join(cards_html)}</div>')
    blocks_html = "\n".join(rows_html_parts)

    links_html = "".join(
        f'<a href="{href_for(l)}" target="_blank" rel="noopener">{l}</a>'
        for l in data["links"]
    )

    cmd = data["setup_command"]
    if is_url(cmd):
        setup_cmd_html = f'<a class="setup-cmd" href="{href_for(cmd)}" target="_blank" rel="noopener">{cmd}</a>'
    else:
        setup_cmd_html = f'<span class="setup-cmd">{cmd}</span>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{data["title"]} {data["subtitle"]}</title>
<link rel="stylesheet" href="posthog-cheatsheet.css">
<style>:root {{ --accent: {data["accent"]}; }}</style>
</head>
<body>
<div class="page">

  <header>
    <div class="brand">
      <div class="logo">{data["icon"]}</div>
      <div>
        <h1>{short_title} {data["subtitle"]}</h1>
        <div class="tagline">{data["tagline"]}</div>
      </div>
    </div>
    <img class="ph-logo ph-logo-header" src="https://posthog.com/brand/posthog-logo-white.svg" alt="PostHog">
  </header>

  <section class="hero">
    <div>
      <h2>Why use it</h2>
      <p>{data["why"]}</p>
    </div>
    <div class="quote">{data["quote"]}</div>
  </section>

  <div class="main">
    {blocks_html}
  </div>

  <footer>
    <div class="setup">
      <b>{data["setup_label"]}</b>
      {setup_cmd_html}
      <div class="setup-meta">{data["setup_meta"]}</div>
    </div>
    <div class="footer-right">
      <div class="links">
        {links_html}
      </div>
    </div>
  </footer>
  <img class="ph-logo ph-logo-bottom" src="https://posthog.com/brand/posthog-logomark.svg" alt="PostHog">

</div>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# Index page
# ---------------------------------------------------------------------------
INDEX_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  background: #f4f1ea; color: #1d1f27;
  min-height: 100vh; padding: 48px 32px;
}
.wrap { max-width: 1100px; margin: 0 auto; }
header {
  background: #1d1f27; color: #fff; border-radius: 12px;
  padding: 28px 32px; margin-bottom: 24px;
  display: flex; align-items: center; justify-content: space-between;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}
.brand { display: flex; align-items: center; gap: 16px; }
.dot {
  width: 48px; height: 48px; background: #f4f1ea; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
}
.dot img { width: 32px; height: 32px; display: block; }
h1 { font-size: 28px; letter-spacing: -0.5px; }
.sub { color: #f4f1ea; opacity: 0.7; font-size: 13px; margin-top: 4px; }
.count {
  background: #eb9d2a; color: #1d1f27; padding: 8px 14px; border-radius: 999px;
  font-weight: 700; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;
}
.grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
}
.card {
  background: #fff; border-radius: 12px; padding: 20px; text-decoration: none;
  color: inherit;
  transition: transform 0.15s, box-shadow 0.15s;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
  display: flex; flex-direction: column; gap: 8px;
}
.card:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.08); }
.card .card-head {
  display: flex; align-items: center; gap: 12px;
}
.card .icon {
  width: 44px; height: 44px; background: var(--accent); border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px; color: #fff;
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 25%, transparent);
  flex-shrink: 0;
}
.card .icon svg { width: 26px; height: 26px; display: block; }
.card h2 { font-size: 20px; letter-spacing: -0.3px; }
.card p { font-size: 12.5px; color: #555; line-height: 1.45; margin-top: 8px; }
.card .arrow {
  margin-top: auto; padding-top: 8px;
  font-size: 12px; color: var(--accent); font-weight: 700;
}
footer {
  margin-top: 32px; text-align: center; color: #999; font-size: 12px;
}
"""

def render_index():
    cards = []
    for slug, data in PAGES.items():
        short_title = data["title"].removeprefix("PostHog ").strip()
        cards.append(f"""
        <a class="card" href="posthog-{slug}.html" target="_blank" rel="noopener" style="--accent: {data['accent']};">
          <div class="card-head">
            <div class="icon">{data['icon']}</div>
            <h2>{short_title}</h2>
          </div>
          <p>{data['summary']}</p>
          <div class="arrow">Open →</div>
        </a>
        """)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>PostHog Cheatsheets: Index</title>
<style>{INDEX_CSS}</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="brand">
      <div class="dot"><img src="https://posthog.com/brand/posthog-logomark.svg" alt="PostHog hedgehog"></div>
      <div>
        <h1>PostHog Cheatsheets</h1>
        <div class="sub">Tips, traps, and real customer patterns for  PostHog product</div>
      </div>
    </div>
    <div class="count">{len(PAGES)} sheets</div>
  </header>

  <div class="grid">
    {"".join(cards)}
  </div>

</div>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# Generate
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    css_path = OUT / "posthog-cheatsheet.css"
    css_path.write_text(BASE_CSS.strip() + "\n", encoding="utf-8")
    print(f"wrote {css_path.name}")

    for slug, data in PAGES.items():
        path = OUT / f"posthog-{slug}.html"
        path.write_text(render_page(slug, data), encoding="utf-8")
        print(f"wrote {path.name}")

    (OUT / "index.html").write_text(render_index(), encoding="utf-8")
    print("wrote index.html")
    print(f"\nDone. {len(PAGES)} cheatsheets + index + shared stylesheet.")
