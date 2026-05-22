#!/usr/bin/env python3
"""Apply context-specific rewrites to generate.py to eliminate em-dashes."""

from pathlib import Path

SRC = Path(__file__).parent / "generate.py"

# Each tuple: (old_string, new_string). Order matters slightly — longer/more
# specific strings first to avoid partial overlaps.
REPLACEMENTS = [
    # ---- Comments
    ("# DATA — one entry per cheatsheet",
     "# DATA. One entry per cheatsheet."),
    ("# Shared CSS — accent is injected per page via a CSS variable",
     "# Shared CSS. The accent color is injected per page via a CSS variable."),

    # ---- Titles & static template strings
    ('<title>{data["title"]} — {data["subtitle"]}</title>',
     '<title>{data["title"]}: {data["subtitle"]}</title>'),
    ('<h1>{data["title"]} — {data["subtitle"]}</h1>',
     '<h1>{data["title"]}: {data["subtitle"]}</h1>'),
    ('<title>PostHog Cheatsheets — Index</title>',
     '<title>PostHog Cheatsheets: Index</title>'),

    # ---- AI page
    ('"Max + MCP — the chat/agent surface for everything PostHog"',
     '"Max + MCP. The chat/agent surface for everything PostHog."'),
    ('"Don\'t use the UI — ask the agent. In-app sidebar, MCP, or Slack: same idea, different surface."',
     '"Don\'t use the UI. Ask the agent. In-app sidebar, MCP, or Slack: same idea, different surface."'),
    ('"In-app sidebar (Max), MCP in your coding agent, PostHog in Slack — same idea, different surface."',
     '"In-app sidebar (Max), MCP in your coding agent, PostHog in Slack: same idea on different surfaces."'),
    ('"quote": "<strong>Don\'t use the UI</strong> — ask the agent to do what you need.",',
     '"quote": "<strong>Don\'t use the UI.</strong> Ask the agent to do what you need.",'),
    ('("Skills", "Reusable instruction units agents call via MCP — teach once, reuse everywhere"),',
     '("Skills", "Reusable instruction units agents call via MCP. Teach once, reuse everywhere."),'),
    ('("MCP calls are almost free — use them in CI.", "Ask “is checkout worse than last week?” <em>before</em> you merge. Cheaper than post-deploy alerts."),',
     '("MCP calls are almost free, so use them in CI.", "Ask “is checkout worse than last week?” <em>before</em> you merge. Cheaper than post-deploy alerts."),'),
    ('("Review every tool call.", "MCP servers are prompt-injection targets — a hostile event could trick an LLM into writing flags. Default to manual approval."),',
     '("Review every tool call.", "MCP servers are prompt-injection targets. A hostile event could trick an LLM into writing flags. Default to manual approval."),'),
    ('("🐘 Dev-first Postgres", "10× YoY", "Consolidated 3+ analytics tools onto PostHog. Used AI for gnarly SQL their PMs couldn\'t write — found AI code-gen as top acquisition channel.", "AI-generated SQL turned a PM bottleneck into a discovery channel."),',
     '("🐘 Dev-first Postgres", "10× YoY", "Consolidated 3+ analytics tools onto PostHog. Used AI for gnarly SQL their PMs couldn\'t write, then found AI code-gen as top acquisition channel.", "AI-generated SQL turned a PM bottleneck into a discovery channel."),'),

    # ---- Cohorts page
    ('"<b>surveys, feature flags, insights, and replay filters</b>. Stop hunting through raw user lists — "',
     '"<b>surveys, feature flags, insights, and replay filters</b>. Stop hunting through raw user lists. "'),
    ('"quote": "<strong>Build once, navigate by it</strong> — chained workflows, per-segment comparisons.",',
     '"quote": "<strong>Build once, navigate by it.</strong> Chained workflows, per-segment comparisons.",'),
    ('("Pin cohorts to your sidebar.", "Multiple customers got lost mid-workflow. The sidebar is customizable — almost nobody discovers this. Cheap win."),',
     '("Pin cohorts to your sidebar.", "Multiple customers got lost mid-workflow. The sidebar is customizable, but almost nobody discovers this. Cheap win."),'),
    ('("🎓 EdTech startup (~900 users)", "~50% response", "PM wanted to survey only students who used the AI tutor “enough.” Built a weekly autocapture → static cohort → re-target loop. Painful but worked.", "Cohorts unlock behavioral targeting even without instrumented events — if you can stomach the refresh tax."),',
     '("🎓 EdTech startup (~900 users)", "~50% response", "PM wanted to survey only students who used the AI tutor “enough.” Built a weekly autocapture → static cohort → re-target loop. Painful but worked.", "Cohorts unlock behavioral targeting even without instrumented events, if you can stomach the refresh tax."),'),

    # ---- Experiments page
    ('"Test causal impact — and do it inside the same tool as your <b>events, flags, replays, and LLM traces</b>. "',
     '"Test causal impact, all inside the same tool as your <b>events, flags, replays, and LLM traces</b>. "'),
    ('("Run an A/A test first.", "Both variants identical. Persistent gap = setup bug — events dropped, users bouncing between variants, bad split."),',
     '("Run an A/A test first.", "Both variants identical. A persistent gap signals a setup bug: events dropped, users bouncing between variants, bad split."),'),
    ('("Don\'t act before you hit sample size.", "Looking is fine — acting on early numbers isn\'t. Watch win prob &amp; effect size over time, not today."),',
     '("Don\'t act before you hit sample size.", "Looking is fine. Acting on early numbers isn\'t. Watch win prob &amp; effect size over time, not today."),'),
    ('("Test the experiment itself with 5–10% first.", "If the variant is broken at 50% rollout, users are contaminated — you can\'t restart cleanly."),',
     '("Test the experiment itself with 5–10% first.", "If the variant is broken at 50% rollout, users are contaminated, and you can\'t restart cleanly."),'),
    ('("🤝 Co-founder matching", "+40% messages", "4-variant test hiding stale profiles at 3/6/9/12 weeks; 6-week won (+35% match acceptance). Same team killed a feature when basically nobody used the minimal version.", "Experiments aren\'t just for picking winners — they\'re for picking <em>how aggressive</em>, and killing without sunk-cost guilt."),',
     '("🤝 Co-founder matching", "+40% messages", "4-variant test hiding stale profiles at 3/6/9/12 weeks; 6-week won (+35% match acceptance). Same team killed a feature when basically nobody used the minimal version.", "Experiments aren\'t just for picking winners. They\'re for picking <em>how aggressive</em>, and killing without sunk-cost guilt."),'),
    ('("⚖️ AI model comparison", "19× volume", "Anonymous-LLM voting product. Every UI change risks skewing rankings — they experiment on everything: button placement, swipe redesigns, AI routers. Event volume 19× in 6 months without ranking drift.", "Experiments aren\'t just about lift — they\'re about not silently breaking the dataset you depend on."),',
     '("⚖️ AI model comparison", "19× volume", "Anonymous-LLM voting product. Every UI change risks skewing rankings, so they experiment on everything: button placement, swipe redesigns, AI routers. Event volume 19× in 6 months without ranking drift.", "Experiments aren\'t just about lift. They\'re about not silently breaking the dataset you depend on."),'),
    ('("⚙️ AI app-building platform", "flags + exp + LLM", "Flags for gradual rollouts, experiments for new ideas, traces for oddness. When GPT-5 shipped weird, they didn\'t guess — they inspected traces and found attention-distribution changes.", "“The change got worse” doesn\'t show up as a crash; you need trace-level data to even notice."),',
     '("⚙️ AI app-building platform", "flags + exp + LLM", "Flags for gradual rollouts, experiments for new ideas, traces for oddness. When GPT-5 shipped weird, they didn\'t guess. They inspected traces and found attention-distribution changes.", "“The change got worse” doesn\'t show up as a crash; you need trace-level data to even notice."),'),

    # ---- Feature Flags page
    ('"tagline": "Decouple deploy from release — ship disabled, flip slowly, watch",',
     '"tagline": "Decouple deploy from release. Ship disabled, flip slowly, watch.",'),
    ('"Feature flags decouple <b>deploy</b> from <b>release</b> — ship disabled, flip for a small %, watch, widen. "',
     '"Feature flags decouple <b>deploy</b> from <b>release</b>. Ship disabled, flip for a small %, watch, widen. "'),
    ('"quote": "<strong>Flag everything</strong> — low cost, free optionality downstream.",',
     '"quote": "<strong>Flag everything.</strong> Low cost, free optionality downstream.",'),
    ('("History tab is your audit log.", "Growth team uses it as primary “what changed and when?” when investigating data anomalies — especially valuable when AI agents have flag access."),',
     '("History tab is your audit log.", "Growth team uses it as primary “what changed and when?” when investigating data anomalies, especially valuable when AI agents have flag access."),'),
    ('("Use flag conditions for survey targeting.", "Skip weekly manual cohort refreshes — flag conditions in survey targeting solve the same problem with no maintenance loop."),',
     '("Use flag conditions for survey targeting.", "Skip weekly manual cohort refreshes. Flag conditions in survey targeting solve the same problem with no maintenance loop."),'),
    ('("🛒 Mid-market ecom (ex-Heap)", "one workflow", "Director of eng listed flags + experiments as explicit pull factors (Heap had neither). First A/B test on a “Shop Now” redesign, used flag-filtered replay to understand <em>why</em>.", "Flags + experiments + replay aren\'t three tools — they\'re one workflow."),',
     '("🛒 Mid-market ecom (ex-Heap)", "one workflow", "Director of eng listed flags + experiments as explicit pull factors (Heap had neither). First A/B test on a “Shop Now” redesign, used flag-filtered replay to understand <em>why</em>.", "Flags + experiments + replay aren\'t three tools. They\'re one workflow."),'),

    # ---- Funnels page
    ('("Funnel = entry point into Replay, not the replay list.", "Strongest pattern across 5+ customers. Funnel acts as a selection filter — raw replay feed is too noisy past a few hundred sessions/day."),',
     '("Funnel = entry point into Replay, not the replay list.", "Strongest pattern across 5+ customers. Funnel acts as a selection filter, since the raw replay feed is too noisy past a few hundred sessions/day."),'),
    ('("Validate UI changes with a funnel <em>before</em> you A/B test.", "Cheap pre-experiment validation — much faster than waiting for a test to power. Saved one team from rolling a regressive age-verification step."),',
     '("Validate UI changes with a funnel <em>before</em> you A/B test.", "Cheap pre-experiment validation, much faster than waiting for a test to power. Saved one team from rolling a regressive age-verification step."),'),
    ('("Tune the mechanics — three settings first-timers leave default.", "<b>Strict vs. unordered</b> · <b>Conversion window</b> (set to your real cycle, not 14 days) · <b>Exclusion steps</b> to filter exit paths."),',
     '("Tune the mechanics. Three settings first-timers leave default.", "<b>Strict vs. unordered</b> · <b>Conversion window</b> (set to your real cycle, not 14 days) · <b>Exclusion steps</b> to filter exit paths."),'),

    # ---- Heatmaps page
    ('"tagline": "Free, near-zero perf cost — clicks, scrolls, movement next to your analytics",',
     '"tagline": "Free, near-zero perf cost for clicks, scrolls, and movement, all next to your analytics.",'),
    ('"already capture — <b>no separate SDK, no consent banner, no billing line</b>. The differentiator: "',
     '"already capture, with <b>no separate SDK, no consent banner, no billing line</b>. The differentiator: "'),
    ('"heatmap data lives next to your analytics — pivot from click cluster → funnel → replay → experiment."',
     '"heatmap data lives next to your analytics, so you can pivot from click cluster → funnel → replay → experiment."'),
    ('("Heatmap", "Position-based", "Clicks/movements by pixel. Clicks don\'t need a clickable element — see where users <em>tried</em> to click on dead pixels. <b>Open for discovery.</b>"),',
     '("Heatmap", "Position-based", "Clicks/movements by pixel. Clicks don\'t need a clickable element. See where users <em>tried</em> to click on dead pixels. <b>Open for discovery.</b>"),'),
    ('("Use the Toolbar, not the in-app Heatmaps scene.", "Toolbar overlays heatmaps on the live site — works on auth-gated pages, catches ~10× more issues, lets you create actions from elements without leaving the page."),',
     '("Use the Toolbar, not the in-app Heatmaps scene.", "Toolbar overlays heatmaps on the live site. Works on auth-gated pages, catches ~10× more issues, lets you create actions from elements without leaving the page."),'),
    ('("🌐 Webshare", "4–5% lifts", "Collapsed Mixpanel + Hotjar + FullStory into PostHog. ~20 experiments at any moment; small UI tweaks drive lifts they wouldn\'t have spotted without heatmap → replay → experiment pointing at the same place.", "It\'s not the heatmap alone — it\'s the heatmap as the trigger for the experiment."),',
     '("🌐 Webshare", "4–5% lifts", "Collapsed Mixpanel + Hotjar + FullStory into PostHog. ~20 experiments at any moment; small UI tweaks drive lifts they wouldn\'t have spotted without heatmap → replay → experiment pointing at the same place.", "It\'s not the heatmap alone. It\'s the heatmap as the trigger for the experiment."),'),
    ('("🤖 Bot detection bonus", "(0, 0) clusters", "Some teams use heatmap click data to flag automated traffic that user-agent strings miss — scripts hammering coordinate <code>(0, 0)</code> to defeat idle timers. Filter them, every insight downstream gets cleaner.", "Heatmaps as a data-quality tool, not just UX."),',
     '("🤖 Bot detection bonus", "(0, 0) clusters", "Some teams use heatmap click data to flag automated traffic that user-agent strings miss, like scripts hammering coordinate <code>(0, 0)</code> to defeat idle timers. Filter them, every insight downstream gets cleaner.", "Heatmaps as a data-quality tool, not just UX."),'),

    # ---- Session Replay page
    ('"tagline": "A re-rendered DOM of what the user actually saw and did — not a video",',
     '"tagline": "A re-rendered DOM of what the user actually saw and did, not a video.",'),
    ('"The strongest pattern is using it as the <em>“why”</em> after some other signal flagged a <em>“what”</em> — "',
     '"The strongest pattern is using it as the <em>“why”</em> after some other signal flagged a <em>“what”</em>, like "'),
    ('"quote": "It also doubles as a <strong>“what\'s weird right now”</strong> radar — abuse, fraud, even inbound-sales signals.",',
     '"quote": "It also doubles as a <strong>“what\'s weird right now”</strong> radar for abuse, fraud, even inbound-sales signals.",'),
    ('("Replay is a DOM, not a video.", "Open the browser inspector mid-playback — elements respond to clicks and hovers. Grab selectors and text without rewatching."),',
     '("Replay is a DOM, not a video.", "Open the browser inspector mid-playback. Elements respond to clicks and hovers. Grab selectors and text without rewatching."),'),
    ('("🎵 Solo SaaS founder", "10,000-store deal", "Watches Replay daily as a fraud + inbound-sales radar. Midnight activity spike → opened the replay expecting abuse → found someone bulk-generating commercial music. Cross-referenced the email, started a sales conversation.", "For the right product, Replay isn\'t retro debugging — it\'s a real-time business signal."),',
     '("🎵 Solo SaaS founder", "10,000-store deal", "Watches Replay daily as a fraud + inbound-sales radar. Midnight activity spike → opened the replay expecting abuse → found someone bulk-generating commercial music. Cross-referenced the email, started a sales conversation.", "For the right product, Replay isn\'t retro debugging. It\'s a real-time business signal."),'),
    ('("🚨 EdTech on-call", "exception → root cause", "Top-15 Replay user at Series B edtech. Backend error fires → opens matching replay → sees the UI state. Found a stale-sidebar bug letting users “request help” on deleted content — invisible in logs alone.", "The bridge from exception to root cause is the killer on-call workflow."),',
     '("🚨 EdTech on-call", "exception → root cause", "Top-15 Replay user at Series B edtech. Backend error fires → opens matching replay → sees the UI state. Found a stale-sidebar bug letting users “request help” on deleted content, all invisible in logs alone.", "The bridge from exception to root cause is the killer on-call workflow."),'),
    ('("☕ Berlin AI startup", "watch parties", "11-person team browses recordings together weekly — partly targeted, partly “morning coffee” mode. Disproved an internal assumption: users gave 2–3 min of thoughtful answers to open-ended quiz prompts.", "Watch parties turn Replay into a team ritual that surfaces qualitative truths dashboards can\'t."),',
     '("☕ Berlin AI startup", "watch parties", "11-person team browses recordings together weekly, partly targeted, partly “morning coffee” mode. Disproved an internal assumption: users gave 2–3 min of thoughtful answers to open-ended quiz prompts.", "Watch parties turn Replay into a team ritual that surfaces qualitative truths dashboards can\'t."),'),
    ('"body": "Some customers use Replay outside analytics entirely — as evidence in legal/fraud cases, and as <em>“you did do that”</em> proof in support tickets and disputes. Not glamorous, but load-bearing for some teams.",',
     '"body": "Some customers use Replay outside analytics entirely, as evidence in legal/fraud cases, and as <em>“you did do that”</em> proof in support tickets and disputes. Not glamorous, but load-bearing for some teams.",'),
]


def main():
    text = SRC.read_text(encoding="utf-8")
    misses = []
    for old, new in REPLACEMENTS:
        if old not in text:
            misses.append(old[:80])
            continue
        text = text.replace(old, new, 1)

    if misses:
        print(f"WARNING: {len(misses)} replacements not found:")
        for m in misses:
            print(f"  - {m!r}")

    remaining = text.count("—")
    print(f"Em-dashes after rewrite: {remaining}")

    SRC.write_text(text, encoding="utf-8")
    print(f"Wrote {SRC}")


if __name__ == "__main__":
    main()
