function shortenURL() {
    const url = document.getElementById("url").value;
    if (!url) {
      alert("Please enter a URL");
      return;
    }
    fetch("http://localhost:5000/shorten", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.shortened) {
          document.getElementById(
            "result"
          ).innerHTML = `Shortened URL: <a href="${data.shortened}" target="_blank">${data.shortened}</a>`;
        } else {
          alert("Error shortening URL");
        }
      });
  }

function unshortenURL() {
    const url = document.getElementById("url").value;
    if (!url) {
        alert("Please enter a URL");
        return;
    }
    fetch("http://localhost:5000/unshorten?" + new URLSearchParams({url: url}), {
        method: "GET",
        headers: { "Content-Type": "application/json" },
    }).then((response) => response.json())
    .then((data) => {
        if(data.unshortened) {
            document.getElementById("result").innerHTML = `Unshortened URL: <a href="${data.unshortened}" target="_blank">${data.unshortened}</a>`
        } else {
            alert("Error unshortening URL");
        }
    })
}