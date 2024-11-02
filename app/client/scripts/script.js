// const fs = require("fs");
let downloadBtn = document.querySelector("download");
let loading_div = document.querySelector("#loading");
let yturl = document.querySelector("#url");
let changeBtn = document.querySelector("#change");
let trackTitle = document.querySelector("#title");
let trackArtist = document.querySelector("#artist");
let trackAlbum = document.querySelector("#album");
let trackGenre = document.querySelector("#genre");
let trackYear = document.querySelector("#year");
let coverString = "";
let convertBtn = document.getElementById("convert-b64");

if (Number.isInteger(document.querySelector("#year"))) {
  console.log("int");
}
let submitBtn = document.querySelector("#submit");

submitBtn.addEventListener("click", () => {
  insertLoad();
  getMp3();
});

function imgToBase64() {
  let cover = document.getElementById("cover");
  let imgFile = cover.files[0];
  // console.log(imgFile);
  // imgB64 = fs;
  if (imgFile) {
    // const base64String = "";
    const reader = new FileReader();
    reader.readAsDataURL(imgFile);
    // console.log(reader.result);
    reader.onload = function () {
      const base64String = reader.result;
      console.log(base64String);
      coverString = base64String.slice(base64String.indexOf(",") + 1);
      console.log(coverString);
    };
  }
}

function insertDownloadButton() {}

function insertLoad() {
  let loading_symbol = document.createElement("div");
  loading_symbol.classList.add("lds-dual-ring");

  // make quote
  let quoteBody = document.createElement("p");
  quoteBody.classList.add("quote");
  let quoteAuthor = document.createElement("p");
  quoteAuthor.classList.add("quote");

  quoteBody.innerHTML =
    "The sky above the port was the color of television tuned to a dead channel";
  quoteAuthor.innerHTML = "William Gibson";

  // TODO: Get quote from server here

  loading_div.innerHTML = null;
  loading_div.appendChild(loading_symbol);
  loading_div.appendChild(quoteBody);
  loading_div.appendChild(quoteAuthor);
}

function cleanup() {
  fetch("http://localhost:8000/cleanup")
    .then((response) => response.json())
    .then((json) => console.log(json));
} // TODO: Make cleanup work, call when file is downloaded. Send request to remove all temp audio files from server

async function getMp3() {
  try {
    // let cover = imgToBase64();
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
        year: trackYear.value,
        cover: coverString,
      }),
      cache: "no-store",
    });

    if (!response.ok) {
      throw new Error(response.statusText);
    }

    let blob = await response.blob();
    let url = URL.createObjectURL(blob);

    let downloadBtn = document.createElement("button");
    downloadBtn.innerHTML = "Download";
    downloadBtn.id = "download";

    let tempAnchor = document.createElement("a");
    tempAnchor.appendChild(downloadBtn);
    tempAnchor.href = url;
    tempAnchor.download = trackTitle.value + ".mp3";
    // document.body.appendChild(tempAnchor);

    loading_div.innerHTML = null;
    loading_div.appendChild(tempAnchor);

    // tempAnchor.click();
    // document.body.removeChild(tempAnchor);
    // URL.revokeObjectURL(url);
  } catch (error) {
    console.error(error);
  }
}

fetch("http://localhost:8000/quote")
  .then((response) => response.json())
  .then((json) => console.log(json));
