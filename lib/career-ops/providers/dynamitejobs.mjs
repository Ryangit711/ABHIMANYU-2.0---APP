// @ts-check
/** @typedef {import('./_types.js').Provider} Provider */

const JOBS_URL = 'https://dynamitejobs.com/jobs';

/** @type {Provider} */
export default {
  id: 'dynamitejobs',

  async fetch(entry, ctx) {
    const text = await ctx.fetchText(JOBS_URL, { redirect: 'error' });
    return parseDynamiteJobsHtml(text);
  },
};

function parseDynamiteJobsHtml(html) {
  if (typeof html !== 'string') return [];
  const jobs = [];

  const jsonLdBlocks = html.match(/<script[^>]*type="application\/ld\+json"[^>]*>([\s\S]*?)<\/script>/gi) || [];
  for (const block of jsonLdBlocks) {
    try {
      const json = JSON.parse(block.replace(/<script[^>]*type="application\/ld\+json"[^>]*>/i, '').replace(/<\/script>/i, ''));
      const items = Array.isArray(json) ? json : (json?.itemListElement || [json]);
      for (const item of items) {
        const job = item?.item || item;
        if (job && job.title) {
          jobs.push({
            title: job.title.trim(),
            url: job.url || '',
            company: (job.hiringOrganization?.name || 'Dynamite Jobs').trim(),
            location: job.jobLocation?.address?.addressLocality || job.jobLocation || '',
            postedAt: job.datePosted ? Date.parse(job.datePosted) : undefined,
          });
        }
      }
    } catch {}
  }

  if (jobs.length > 0) return jobs;

  const blocks = html.match(/<div[^>]*class="[^"]*job[^"]*"[^>]*>[\s\S]*?<\/div>/gi) || [];
  for (const block of blocks) {
    const titleMatch = block.match(/<h[23][^>]*>([\s\S]*?)<\/h[23]>/i) || block.match(/<a[^>]*class="[^"]*title[^"]*"[^>]*>([\s\S]*?)<\/a>/i);
    if (!titleMatch) continue;
    const title = titleMatch[1].replace(/<[^>]+>/g, '').trim();
    if (!title) continue;

    const linkMatch = block.match(/href="(https?:\/\/[^"]+)"/);
    const url = linkMatch ? linkMatch[1] : '';

    const companyMatch = block.match(/<span[^>]*class="[^"]*company[^"]*"[^>]*>([\s\S]*?)<\/span>/i);
    const company = companyMatch ? companyMatch[1].replace(/<[^>]+>/g, '').trim() : 'Dynamite Jobs';

    const locationMatch = block.match(/location[^:]*:\s*([^<,]+)/i);
    const location = locationMatch ? locationMatch[1].trim() : '';

    jobs.push({ title, url, company, location });
  }

  return jobs;
}
