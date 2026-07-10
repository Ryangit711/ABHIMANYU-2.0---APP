// @ts-check
/** @typedef {import('./_types.js').Provider} Provider */

const FEED_URL = 'https://www.eluta.ca/opensearch';

/** @type {Provider} */
export default {
  id: 'elutaca',

  async fetch(entry, ctx) {
    const query = entry?.search_query || 'operations+strategy+manager+director';
    const feedUrl = `${FEED_URL}?q=${encodeURIComponent(query)}&search=Search`;
    let text;
    try {
      text = await ctx.fetchText(feedUrl, { redirect: 'error' });
    } catch {
      return [];
    }
    return parseElutaXml(text);
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
    return parsed.protocol === 'https:' ? parsed.href : '';
  } catch {
    return '';
  }
}

function parseElutaXml(xml) {
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
    const company = tagText(item, 'company');

    const locationMatch = description ? description.match(/(Vancouver|British Columbia|BC|Remote|Canada)/i) : null;
    const location = locationMatch ? locationMatch[0] : '';

    let salary = '';
    const salaryMatch = description ? description.match(/\$[\d,]+(?:\s*-\s*\$[\d,]+)?/g) : null;
    if (salaryMatch) salary = salaryMatch[0];

    jobs.push({
      title: rawTitle,
      company: company || 'Eluta.ca',
      location,
      url,
      postedAt: pubDate ? Date.parse(pubDate) : undefined,
      salary,
    });
  }

  return jobs;
}
