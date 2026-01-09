import fetch from "node-fetch";

export default async function handler(req, res) {
  const targetUrl = req.query.url;
  if (!targetUrl) {
    return res.status(400).json({ error: "Missing 'url' query parameter" });
  }

  // Validate URL
  try {
    new URL(targetUrl);
  } catch {
    return res.status(400).json({ error: "Invalid URL" });
  }

  try {
    const response = await fetch(targetUrl, {
      headers: { "User-Agent": "Node Proxy Server" },
      timeout: 10000
    });

    const text = await response.text();

    try {
      const data = JSON.parse(text);
      return res.json(data);
    } catch {
      return res.status(502).json({
        error: "Invalid JSON from target",
        status_code: response.status,
        content: text.slice(0, 500)
      });
    }
  } catch (err) {
    return res.status(500).json({ error: "Request failed", details: err.message });
  }
}
