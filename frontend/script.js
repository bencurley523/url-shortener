const API_BASE = "http://localhost:8000";

async function shortenUrl() {
    const longUrl = document.getElementById('longUrl').value;
    const customAlias = document.getElementById('customAlias').value;
    const errorMsg = document.getElementById('shortenerError');
    const outputBox = document.getElementById('shortenerOutput');
    const resultLink = document.getElementById('shortLinkResult');

    // Reset UI
    errorMsg.innerText = "";
    outputBox.style.display = 'none';

    if (!longUrl) {
        errorMsg.innerText = "Please enter a URL first!";
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/shorten`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ longUrl, custom_alias: customAlias || null })
        });

        const data = await response.json();

        if (!response.ok) {
            errorMsg.innerText = data.detail || "Error shortening URL";
            return;
        }

        // Show Success
        const fullShortUrl = `${API_BASE}/${data.shortUrl}`;
        resultLink.href = fullShortUrl;
        resultLink.innerText = fullShortUrl;
        outputBox.style.display = 'block';

    } catch (error) {
        errorMsg.innerText = "Could not connect to server.";
    }
}

async function checkStats() {
    const shortCode = document.getElementById('statsInput').value.trim();
    const errorMsg = document.getElementById('statsError');
    const outputBox = document.getElementById('statsOutput');

    // Reset UI
    errorMsg.innerText = "";
    outputBox.style.display = 'none';

    if (!shortCode) {
        errorMsg.innerText = "Please enter a short code.";
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/stats/${shortCode}`);
        
        if (!response.ok) {
            if (response.status === 404) {
                errorMsg.innerText = "Short URL not found.";
            } else if (response.status === 429) {
                errorMsg.innerText = "Too many requests.";
            } else {
                errorMsg.innerText = "Error fetching stats.";
            }
            return;
        }

        const data = await response.json();

        // Update Data
        document.getElementById('clickCount').innerText = data.clicks;
        document.getElementById('originalLink').innerText = data.longUrl.slice(0, 35) + "...";
        document.getElementById('originalLink').href = data.longUrl;

        if (data.last_accessed) {
            document.getElementById('lastAccessed').innerText = new Date(data.last_accessed).toLocaleString();
        } else {
            document.getElementById('lastAccessed').innerText = "Never";
        }

        // Show Box
        outputBox.style.display = 'block';

    } catch (error) {
        errorMsg.innerText = "Could not connect to server.";
        console.error(error);
    }
}

function copyToClipboard() {
    const urlText = document.getElementById('shortLinkResult').innerText;
    navigator.clipboard.writeText(urlText);
    alert("Copied to clipboard!"); // Keeping this simple alert is usually fine for 'copy' actions
}