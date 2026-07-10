// @ts-check
/** @typedef {import('./_types.js').Provider} Provider */

const FEED_URL = 'http://rss.jobsearch.monster.com/rssquery.ashx';

/** @type {Provider} */
export default {
  id: 'monsterca',

  async fetch(entry, ctx) {
    const query = entry?.search_query || 'operations strategy director manager';
    const location = entry?.search_location || 'Vancouver BC';
    const feedUrl = `${FEED_URL}?q=${encodeURIComponent(query)}&where=${encodeURIComponent(location)}&page=1`;
    const text = await ctx.fetchText(feedUrl, { redirect: 'error' });
    return parseMonsterFeed(text, entry?.name || 'Monster.ca');
  },
};

function extractText(inner) {
  const cdata = inner.match(/^\s*<!\[CDATA\[([\s\S]*?)\]\]>\s*$/);
  if (cdata) return cdata[1].trim();
  return inner.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&apos;/g, "'").trim();
}

function tagText(block, tag) {
  const m = block.match(new RegExp(`<${tag}\\b[^>]*>([\\s\\S]*?)</${tag}>`, 'i'));
  return m ? extractText(m[1]) : '';
}

function cleanUrl(value) {
  if (!value) return '';
  const trimmed = value.trim();
  try {
    const parsed = new URL(trimmed);
    return parsed.protocol === 'https:' || parsed.protocol === 'http:' ? parsed.href : '';
  } catch {
    return '';
  }
}

function parseMonsterFeed(xml, defaultCompany) {
  if (typeof xml !== 'string') return [];
  const jobs = [];
  const blocks = xml.match(/<item\b[^>]*>[\s\S]*?<\/item>/gi) || [];

  for (const item of blocks) {
    const url = cleanUrl(tagText(item, 'link'));
    if (!url) continue;

    const rawTitle = tagText(item, 'title');
    if (!rawTitle) continue;

    const description = tagText(item, 'description');
    const pubDate = tagText(item, 'pubDate');

    jobs.push({
      title: rawTitle,
      company: defaultCompany,
      location: '',
      url,
      postedAt: pubDate ? Date.parse(pubDate) : undefined,
      description,
    });
  }

  return jobs;
}
