async function shortenUrl() {
    const input = document.getElementById('longUrl').value;
    const alias = document.getElementById('custom_alias').value;
    const resultDiv = document.getElementById('result');
    const shortLink = document.getElementById('shortLink');
    const errorMsg = document.getElementById('error');

    // 1. Clear previous results/errors
    resultDiv.classList.add('hidden');
    errorMsg.innerText = "";

    if (!input) {
        errorMsg.innerText = "Please enter a URL.";
        return;
    }

    const payload = { longUrl: input };
    if (alias) {
        payload.custom_alias = alias;
    }

    try {
        // 2. Send POST request to your FastAPI backend
        const response = await fetch('http://127.0.0.1:8000/shorten', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            if (response.status === 400) {
                throw new Error("That alias is already taken.");
            }
            throw new Error('Server returned error');
        }

        const data = await response.json();

        // 3. Construct the full short URL (Backend only gives code, e.g., "eyWH")
        // We assume your backend is running on port 8000
        const fullShortUrl = `http://127.0.0.1:8000/${data.shortUrl}`;

        // 4. Update the UI
        shortLink.href = fullShortUrl;
        shortLink.innerText = fullShortUrl;
        resultDiv.classList.remove('hidden'); // Show the result

    } catch (err) {
        console.error(err);
        errorMsg.innerText = err.message || "Failed to shorten URL.";
    }
}