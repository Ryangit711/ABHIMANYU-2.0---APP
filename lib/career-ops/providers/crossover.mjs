// @ts-check
/** @typedef {import('./_types.js').Provider} Provider */

const JOBS_URL = 'https://www.crossover.com/jobs/';

/** @type {Provider} */
export default {
  id: 'crossover',

  async fetch(entry, ctx) {
    const text = await ctx.fetchText(JOBS_URL, { redirect: 'error' });
    return parseCrossoverHtml(text);
  },
};

function parseCrossoverHtml(html) {
  if (typeof html !== 'string') return [];
  const jobs = [];

  const jobBlocks = html.match(/<div[^>]*class="[^"]*job-card[^"]*"[^>]*>[\s\S]*?<\/div>\s*<\/div>\s*<\/div>/gi)
    || html.match(/<article[^>]*>[\s\S]*?<\/article>/gi)
    || [];

  if (jobBlocks.length === 0) {
    const scriptBlocks = html.match(/<script[^>]*>[\s\S]*?<\/script>/gi) || [];
    for (const script of scriptBlocks) {
      const jsonMatch = script.match(/window\.__INITIAL_STATE__\s*=\s*({[\s\S]*?});/);
      if (jsonMatch) {
        try {
          const state = JSON.parse(jsonMatch[1]);
          const items = state?.jobs?.items || state?.results || [];
          for (const j of items) {
            if (j.title) {
              jobs.push({
                title: j.title.trim(),
                url: j.url || j.applyUrl || '',
                company: j.company || j.companyName || 'Crossover',
                location: j.location || j.remote === true ? 'Remote' : '',
                salary: j.salary || j.salaryRange || '',
              });
            }
          }
        } catch {}
      }
    }
    return jobs;
  }

  for (const block of jobBlocks) {
    const titleMatch = block.match(/<h[23][^>]*>([\s\S]*?)<\/h[23]>/i);
    if (!titleMatch) continue;
    const title = titleMatch[1].replace(/<[^>]+>/g, '').trim();
    if (!title) continue;

    const linkMatch = block.match(/href="(https?:\/\/[^"]+)"/);
    const url = linkMatch ? linkMatch[1] : '';

    const companyMatch = block.match(/<span[^>]*class="[^"]*company[^"]*"[^>]*>([\s\S]*?)<\/span>/i);
    const company = companyMatch ? companyMatch[1].replace(/<[^>]+>/g, '').trim() : 'Crossover';

    const locationMatch = block.match(/location[^:]*:\s*([^<]+)/i);
    const location = locationMatch ? locationMatch[1].trim() : 'Remote';

    const salaryMatch = block.match(/\$[\d,]+(?:\s*-\s*\$[\d,]+)?\/\w+/g);
    const salary = salaryMatch ? salaryMatch[0] : '';

    jobs.push({ title, url, company, location, salary });
  }

  return jobs;
}
