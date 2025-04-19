// change 'local' to 'production' for production use



function shortenURL(custom=false) { //shortens and shows url block

    // 1. shortens URL
    // 2. shows url block with the copy button
    // 3. changes the 'copy' text to 'copied' when user clicks on it
    // 4. resets the 'copied' button to 'copy' when user shortens again


    const url = document.getElementById("url").value;
    const custom_key = document.getElementById("custom-key").value;
    let requestbody = {url: url};
    if (custom) {
      if(custom_key.length == 0) {
        alert("Please enter a custom key");
        return;
      }
      requestbody.custom_key = custom_key;
    }
    if (!url) {
      alert("Please enter a URL");
      return;
    }

    fetch(`${conf.local.api_url}/shorten`, { // change to production URL
      method: "POST",
      headers: { "Content-Type": "application/json"},
      body: JSON.stringify(requestbody),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.shortened) {
          
          let b = document.getElementById("url-block");
          let p = document.getElementById("result");
          
          p.innerHTML = `Shortened URL: <a href="http://${data.shortened}" target="_blank">${data.shortened}</a>`;
          b.style.display = "block"

        } else {
          alert(`Error shortening URL: ${data.error}`);
        }
      });
    
  }

function unshortenURL() {
    const url = document.getElementById("url").value;
    if (!url) {
        alert("Please enter a URL");
        return;
    }
    fetch(`${conf.local.api_url}/unshorten?` + new URLSearchParams({url: url}), { // change to production URL
        method: "GET",
        headers: { "Content-Type": "application/json" },
    }).then((response) => response.json())
    .then((data) => {
        if(data.unshortened) {
            let p = document.getElementById("result")
            let b = document.getElementById("url-block");
            p.innerHTML = `Unshortened URL: <a href="${data.unshortened}" target="_blank">${data.unshortened}</a>`;
            b.style.display = "block"
        } else {
            alert(`Error unshortening URL:${data.error}`);
        }
    })
}


function toggleCopy() {
    let copyButton = document.getElementById("copy-button");
    
    if (copyButton.innerHTML === "Copy") {
      let p = document.getElementById("result");
      let url = p.querySelector("a").href;
      navigator.clipboard.writeText(url);
      copyButton.innerHTML = "Copied!";
      copyButton.classList.remove("btn-light");
      copyButton.classList.add("btn-success");
      setTimeout(() => {
        copyButton.innerHTML = "Copy";
        copyButton.classList.add("btn-light");
        copyButton.classList.remove("btn-success");
      }, 2500);
    } else if (copyButton.innerHTML === "Copied!") {
      copyButton.innerHTML = "Copy";
    }
}

function toggleCustom() {
    let customKey = document.getElementById("custom-key");
    
    if (customKey.style.display === "none") {
        customKey.style.display = "block";
        
    } else {
        customKey.style.display = "none";
        shortenURL(custom=true);
    }
}