// @ts-check
/** @typedef {import('./_types.js').Provider} Provider */

const JOBS_URL = 'https://trulyremote.co/jobs';

/** @type {Provider} */
export default {
  id: 'trulyremote',

  async fetch(entry, ctx) {
    const text = await ctx.fetchText(JOBS_URL, { redirect: 'error' });
    return parseTrulyRemoteHtml(text);
  },
};

function parseTrulyRemoteHtml(html) {
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

    const companyMatch = block.match(/class="[^"]*company[^"]*"[^>]*>([\s\S]*?)</i);
    const company = companyMatch ? companyMatch[1].replace(/<[^>]+>/g, '').trim() : 'Truly Remote';

    const locationMatch = block.match(/class="[^"]*location[^"]*"[^>]*>([\s\S]*?)</i);
    const location = locationMatch ? locationMatch[1].replace(/<[^>]+>/g, '').trim() : 'Remote';

    jobs.push({ title, url, company, location });
  }

  return jobs;
}
