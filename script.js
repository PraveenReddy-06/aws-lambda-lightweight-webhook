const $ = (id) => document.getElementById(id);

$("send").addEventListener("click", async () => {
  const url = $("url").value.trim();
  const secret = $("secret").value;
  const eventType = $("eventType").value;
  const projectName = $("projectName").value.trim();

  const eventId = "web-" + Date.now();

  const payload = {
    eventId,
    eventType,
    source: "LightweightWebhookFrontend",
    data: {
      projectName
    }
  };

  $("status").textContent = "Sending...";
  $("output").textContent = JSON.stringify(payload, null, 2);

  try {
    const res = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Webhook-Secret": secret
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    $("status").textContent = res.status + " " + res.statusText;
    $("output").textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    $("status").textContent = "Request failed";
    $("output").textContent =
      "Browser request failed. Check Function URL CORS configuration.\n\n" +
      error.message;
  }
});