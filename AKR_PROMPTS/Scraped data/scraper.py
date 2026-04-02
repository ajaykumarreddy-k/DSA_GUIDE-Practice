"""
motionsites.ai scraper
Strategy:
  1. Intercept all network responses to find JSON data with prompts
  2. Load the page fully, dump the entire rendered DOM
  3. Parse cards from DOM: title, category, gif/video url, prompt text
  4. As fallback: hover each card to reveal the Copy button, click it, read clipboard
  5. Download all GIFs and save results.json
"""

import asyncio
import json
import re
from pathlib import Path

import httpx
from playwright.async_api import async_playwright, Page
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# ── 1. Network interception: catch any JSON response that looks like prompt data ──
intercepted: list[dict] = []

async def handle_response(response):
    try:
        ct = response.headers.get("content-type", "")
        if "json" in ct and response.status == 200:
            url = response.url
            if any(k in url for k in ["prompt", "site", "template", "card", "data", "api"]):
                body = await response.json()
                intercepted.append({"url": url, "body": body})
    except Exception:
        pass


async def scrape() -> list[dict]:
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
        context = await browser.new_context(
            permissions=["clipboard-read", "clipboard-write"],
        )
        page = await context.new_page()

        # Intercept network
        page.on("response", lambda r: asyncio.ensure_future(handle_response(r)))

        console.print("[bold cyan]Loading motionsites.ai …[/]")
        await page.goto("https://motionsites.ai/", wait_until="networkidle", timeout=90_000)
        await asyncio.sleep(3)

        # ── Scroll to trigger lazy loading ───────────────────────────────────
        console.print("[cyan]Scrolling to load all cards …[/]")
        prev_h = 0
        for _ in range(50):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(1.0)
            h = await page.evaluate("document.body.scrollHeight")
            if h == prev_h:
                break
            prev_h = h
        await asyncio.sleep(2)

        # ── Dump full page HTML to inspect structure ──────────────────────────
        html = await page.content()
        Path("output/page_dump.html").write_text(html, encoding="utf-8")
        console.print("[dim]Page HTML saved to output/page_dump.html[/]")

        # ── Check intercepted JSON for prompt data ────────────────────────────
        console.print(f"[dim]Intercepted {len(intercepted)} JSON responses[/]")
        for item in intercepted:
            console.print(f"  [dim]{item['url']}[/]")
        Path("output/intercepted.json").write_text(
            json.dumps(intercepted, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # ── Extract all card data from DOM ────────────────────────────────────
        cards = await page.evaluate("""
        () => {
            const results = [];

            // Print all unique tag+class combos to help debug
            const allEls = [...document.querySelectorAll('*')];
            const combos = new Set();
            allEls.forEach(el => {
                if (el.className && typeof el.className === 'string') {
                    el.className.split(' ').forEach(c => {
                        if (c) combos.add(el.tagName.toLowerCase() + '.' + c);
                    });
                }
            });

            // Find cards: elements that have an img AND sibling text AND are repeated
            // Try every div that directly contains an img + some text content
            const candidates = [...document.querySelectorAll('div, article, li, section')].filter(el => {
                const hasImg = el.querySelector('img, video');
                const text = (el.innerText || '').trim();
                const rect = el.getBoundingClientRect();
                return hasImg && text.length > 5 && rect.width > 100 && rect.height > 100
                    && rect.width < 800 && el.children.length >= 1 && el.children.length <= 20;
            });

            // Score each candidate: prefer ones with multiple siblings of similar size
            const scored = candidates.map(el => {
                const siblings = el.parentElement
                    ? [...el.parentElement.children].filter(c => c !== el).length
                    : 0;
                return { el, siblings };
            }).filter(x => x.siblings >= 2);

            // Sort by sibling count desc (most repeated = most likely grid cards)
            scored.sort((a, b) => b.siblings - a.siblings);

            const seen = new Set();
            for (const { el } of scored.slice(0, 200)) {
                const img = el.querySelector('img');
                const video = el.querySelector('video');
                const gifUrl = img?.src || video?.src || img?.dataset?.src || '';

                if (!gifUrl || gifUrl.includes('logo') || gifUrl.includes('icon') ||
                    gifUrl.includes('avatar') || gifUrl.includes('facebook')) continue;
                if (seen.has(gifUrl)) continue;
                seen.add(gifUrl);

                // All text content split by lines
                const lines = (el.innerText || '').trim().split('\\n')
                    .map(l => l.trim()).filter(l => l.length > 0);

                // Title: usually first short line
                const title = lines.find(l => l.length > 2 && l.length < 60 &&
                    !['copy','premium','free'].includes(l.toLowerCase())) || '';

                // Category: often "Landing Page", "SaaS", etc.
                const category = lines.find(l =>
                    ['landing page','saas','portfolio','ecommerce','agency',
                     'startup','blog','dashboard'].some(k => l.toLowerCase().includes(k))
                ) || '';

                // Prompt: longest line or paragraph
                const prompt = lines.reduce((a, b) => b.length > a.length ? b : a, '');

                // Get all text for inspection
                const allText = lines.join(' | ');

                results.push({ gif_url: gifUrl, title, category, prompt, allText });
            }

            return results;
        }
        """)

        console.print(f"[green]DOM extraction found {len(cards)} cards[/]")

        # ── Hover + click Copy on each visible card ───────────────────────────
        console.print("[cyan]Attempting to click Copy buttons via hover …[/]")
        await page.evaluate("window.scrollTo(0, 0)")
        await asyncio.sleep(1)

        results = []
        card_elements = await page.query_selector_all("div, article, li")

        # Filter to only those that have an img and some text
        valid_cards = []
        for el in card_elements:
            try:
                img = await el.query_selector("img, video")
                text = (await el.inner_text()).strip()
                if img and len(text) > 5:
                    src = await el.evaluate("""
                        el => {
                            const img = el.querySelector('img');
                            const vid = el.querySelector('video');
                            return img?.src || vid?.src || '';
                        }
                    """)
                    if (src and 'logo' not in src and 'icon' not in src
                            and 'facebook' not in src and 'avatar' not in src):
                        valid_cards.append((el, src, text))
            except Exception:
                pass

        console.print(f"[dim]Valid card elements: {len(valid_cards)}[/]")

        seen_urls = set()
        with Progress(
            SpinnerColumn(), TextColumn("{task.description}"),
            BarColumn(), TextColumn("{task.completed}/{task.total}"),
            console=console,
        ) as prog:
            task = prog.add_task("Processing cards", total=min(len(valid_cards), 150))

            for el, gif_url, raw_text in valid_cards[:150]:
                if gif_url in seen_urls:
                    prog.advance(task)
                    continue
                seen_urls.add(gif_url)

                prompt = ""
                title = ""
                category = ""

                try:
                    await el.scroll_into_view_if_needed()
                    await asyncio.sleep(0.2)
                    await el.hover()
                    await asyncio.sleep(0.4)

                    # Look for Copy button that appeared after hover
                    btn = await el.query_selector("button")
                    if not btn:
                        # Try page-level search near this element
                        all_btns = await page.query_selector_all("button")
                        for b in all_btns:
                            t = (await b.inner_text()).strip().lower()
                            if t in ("copy", "copy prompt"):
                                btn = b
                                break

                    if btn:
                        btn_text = (await btn.inner_text()).strip().lower()
                        if btn_text in ("copy", "copy prompt"):
                            await page.evaluate("navigator.clipboard.writeText('')")
                            await btn.click()
                            await asyncio.sleep(0.5)
                            prompt = (await page.evaluate("navigator.clipboard.readText()")).strip()

                    # Parse title and category from raw text
                    lines = [l.strip() for l in raw_text.split('\n') if l.strip()]
                    title = next((l for l in lines if 2 < len(l) < 60
                                  and l.lower() not in ('copy','premium','free')), '')
                    category = next((l for l in lines if any(
                        k in l.lower() for k in ['landing','saas','portfolio','ecommerce',
                                                  'agency','startup','blog','dashboard']
                    )), '')

                    if not prompt:
                        # Fallback: longest line
                        prompt = max(lines, key=len) if lines else ''

                except Exception as e:
                    console.print(f"[red dim]  card error: {e}[/]")

                results.append({
                    "title": title,
                    "category": category,
                    "gif_url": gif_url,
                    "prompt": prompt,
                    "raw_text": raw_text[:300],
                })
                prog.advance(task)

        await browser.close()

    console.print(f"[bold green]Collected {len(results)} entries[/]")
    return results


async def download_gif(client: httpx.AsyncClient, url: str, filename: str) -> bool:
    try:
        r = await client.get(url, follow_redirects=True, timeout=30)
        if r.status_code == 200:
            (OUTPUT_DIR / filename).write_bytes(r.content)
            return True
    except Exception as e:
        console.print(f"[red]  ✗ {url}: {e}[/]")
    return False


async def download_all(items: list[dict]) -> list[dict]:
    async with httpx.AsyncClient(headers={"User-Agent": "Mozilla/5.0"}) as client:
        with Progress(
            SpinnerColumn(), TextColumn("{task.description}"),
            BarColumn(), TextColumn("{task.completed}/{task.total}"),
            console=console,
        ) as progress:
            task = progress.add_task("Downloading GIFs …", total=len(items))
            for i, item in enumerate(items):
                url = item.get("gif_url", "")
                if url:
                    ext = Path(url.split("?")[0]).suffix or ".gif"
                    filename = f"prompt_{i+1:04d}{ext}"
                    ok = await download_gif(client, url, filename)
                    item["local_file"] = filename if ok else None
                else:
                    item["local_file"] = None
                progress.advance(task)
    return items


async def main() -> None:
    console.rule("[bold magenta]motionsites.ai scraper[/]")
    items = await scrape()

    if not items:
        console.print("[bold red]Nothing found — check output/page_dump.html to inspect the DOM.[/]")
        return

    items = await download_all(items)

    out = OUTPUT_DIR / "results.json"
    out.write_text(json.dumps(items, indent=2, ensure_ascii=False))
    console.print(f"\n[bold green]✓ {len(items)} entries → {out}[/]")

    console.print("\n[bold underline]── Sample ──[/]")
    for item in items[:5]:
        console.print(f"  [yellow]{item.get('local_file')}[/]")
        console.print(f"    title:    {item.get('title')}")
        console.print(f"    category: {item.get('category')}")
        console.print(f"    prompt:   {item.get('prompt', '')[:100]}")
        console.print()


if __name__ == "__main__":
    asyncio.run(main())

