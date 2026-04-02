const DEFAULT_TIMEOUT_MESSAGE =
  "Set VERCEL_BACKEND_URL in Netlify environment variables so this function can proxy requests to the Vercel Python API.";

function jsonResponse(status, payload) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "access-control-allow-origin": "*",
      "access-control-allow-methods": "GET, POST, OPTIONS",
      "access-control-allow-headers": "content-type",
    },
  });
}

export default async (request) => {
  if (request.method === "OPTIONS") {
    return new Response(null, {
      status: 204,
      headers: {
        "access-control-allow-origin": "*",
        "access-control-allow-methods": "GET, POST, OPTIONS",
        "access-control-allow-headers": "content-type",
      },
    });
  }

  const backend = process.env.VERCEL_BACKEND_URL;
  if (!backend) {
    return jsonResponse(500, {
      error: DEFAULT_TIMEOUT_MESSAGE,
      recommendation:
        "Netlify's current Functions docs focus on Node, TypeScript, and Go runtimes, so this project proxies API traffic to the Vercel Python deployment for the most reliable setup.",
    });
  }

  const sourceUrl = new URL(request.url);
  const upstream = new URL(backend);
  upstream.search = sourceUrl.search;

  const init = {
    method: request.method,
    headers: { "content-type": request.headers.get("content-type") || "application/json" },
  };

  if (request.method !== "GET" && request.method !== "HEAD") {
    init.body = await request.text();
  }

  const response = await fetch(upstream, init);
  const text = await response.text();
  return new Response(text, {
    status: response.status,
    headers: {
      "content-type": response.headers.get("content-type") || "application/json; charset=utf-8",
      "access-control-allow-origin": "*",
      "access-control-allow-methods": "GET, POST, OPTIONS",
      "access-control-allow-headers": "content-type",
    },
  });
};
