// @ts-check
/** @typedef {import('./_types.js').Provider} Provider */

const JOBS_URL = 'https://collabwork.com/jobs';

/** @type {Provider} */
export default {
  id: 'collabwork',

  async fetch(entry, ctx) {
    const text = await ctx.fetchText(JOBS_URL, { redirect: 'error' });
    return parseCollabworkHtml(text);
  },
};

function parseCollabworkHtml(html) {
  if (typeof html !== 'string') return [];
  const jobs = [];

  const blocks = html.match(/<div[^>]*class="[^"]*job[^"]*"[^>]*>[\s\S]*?<\/div>/gi) || [];
  for (const block of blocks) {
    const titleMatch = block.match(/<h[23][^>]*>([\s\S]*?)<\/h[23]>/i);
    if (!titleMatch) continue;
    const title = titleMatch[1].replace(/<[^>]+>/g, '').trim();
    if (!title) continue;

    const linkMatch = block.match(/href="(https?:\/\/[^"]+)"/);
    const url = linkMatch ? linkMatch[1] : '';

    const companyMatch = block.match(/company[^:]*:\s*([^<,]+)/i) || block.match(/at\s+([A-Z][^<,]+?)(?:\s*\||\s*–|\s*—|,)/i);
    const company = companyMatch ? companyMatch[1].trim() : 'CollabWork';

    const locationMatch = block.match(/location[^:]*:\s*([^<,]+)/i);
    const location = locationMatch ? locationMatch[1].trim() : '';

    jobs.push({ title, url, company, location });
  }

  return jobs;
}
