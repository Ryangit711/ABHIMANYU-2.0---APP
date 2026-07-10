// @ts-check
/** @typedef {import('./_types.js').Provider} Provider */

const FEED_URL = 'https://hiring.cafe/api/jobs';

/** @type {Provider} */
export default {
  id: 'hiringcafe',

  async fetch(entry, ctx) {
    const query = entry?.search_query || 'operations strategy manager director';
    const url = `${FEED_URL}?q=${encodeURIComponent(query)}&limit=100`;
    let json;
    try {
      json = await ctx.fetchJson(url, { redirect: 'error' });
    } catch {
      return [];
    }

    const jobs = Array.isArray(json) ? json : (json?.jobs || json?.data || []);
    if (!Array.isArray(jobs)) return [];

    return jobs
      .filter(j => j && typeof j === 'object' && typeof (j.title || j.position) === 'string')
      .map(j => ({
        title: (j.title || j.position || '').trim(),
        url: (j.url || j.apply_url || j.link || '').trim(),
        company: (j.company_name || j.company || j.organization || entry?.name || 'Hiring Cafe').trim(),
        location: (j.location || j.candidate_required_location || '').trim(),
        salary: j.salary || j.compensation || '',
        postedAt: j.created_at || j.posted_at || j.date || undefined,
      }));
  },
};
