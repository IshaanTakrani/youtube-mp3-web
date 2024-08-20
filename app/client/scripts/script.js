let downloadBtn = document.querySelector("download");
let loading_div = document.querySelector("#loading");
let yturl = document.querySelector("#url");
let changeBtn = document.querySelector("#change");
let trackTitle = document.querySelector("#title");
let trackArtist = document.querySelector("#artist");
let trackAlbum = document.querySelector("#album");
let trackGenre = document.querySelector("#genre");

function insertDownloadButton() {
  let downloadBtn = document.createElement("button");
  downloadBtn.innerHTML = "Download";
  downloadBtn.id = "download";

  loading_div.innerHTML = null;
  loading_div.appendChild(downloadBtn);
}

function insertLoad() {
  let loading_symbol = document.createElement("div");
  loading_symbol.classList.add("lds-dual-ring");
  loading_div.innerHTML = null;
  loading_div.appendChild(loading_symbol);
}

function cleanup() {} // TODO: Make cleanup work, call when file is downloaded. Send request to remove all temp audio files from server

async function getMp3() {
  try {
    let response = await fetch("http://localhost:8000/submit-tag-data", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        url: yturl.value,
        title: trackTitle.value,
        artist: trackArtist.value,
        album: trackAlbum.value,
        genre: trackGenre.value,
      }),
      cache: "no-store",
    });

    if (!response.ok) {
      throw new Error(response.statusText);
    }

    let blob = await response.blob();
    let url = URL.createObjectURL(blob);
    let tempAnchor = document.createElement("a");
    tempAnchor.href = url;
    tempAnchor.download = trackTitle.value + ".mp3";
    document.body.appendChild(tempAnchor);
    tempAnchor.click();
    document.body.removeChild(tempAnchor);
    URL.revokeObjectURL(url);
  } catch (error) {
    console.error(error);
  }
}
