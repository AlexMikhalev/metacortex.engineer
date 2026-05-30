export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    let key = url.pathname.slice(1);

    if (key === "" || key === "/") {
      key = "index.html";
    } else if (key.endsWith("/")) {
      key = key + "index.html";
    }

    let object = await env.BUCKET.get(key);

    if (!object) {
      object = await env.BUCKET.get(key + "/index.html");
    }

    if (!object && key.includes("/") && !key.endsWith(".html")) {
      const parent = key.substring(0, key.lastIndexOf("/") + 1);
      if (parent) object = await env.BUCKET.get(parent + "index.html");
    }

    if (!object) {
      return new Response("Not Found", { status: 404 });
    }

    const headers = new Headers();
    object.writeHttpMetadata(headers);
    headers.set("etag", object.httpEtag);
    headers.set("cache-control", "public, max-age=3600");

    const ext = key.split(".").pop().toLowerCase();
    const types = {
      html: "text/html;charset=utf-8",
      css: "text/css;charset=utf-8",
      js: "application/javascript",
      json: "application/json",
      xml: "application/xml",
      png: "image/png",
      jpg: "image/jpeg",
      jpeg: "image/jpeg",
      gif: "image/gif",
      svg: "image/svg+xml",
      ico: "image/x-icon",
      webp: "image/webp",
      woff: "font/woff",
      woff2: "font/woff2",
      ttf: "font/ttf",
      pdf: "application/pdf",
      txt: "text/plain",
    };
    if (types[ext]) headers.set("content-type", types[ext]);

    return new Response(object.body, { headers });
  },
};
