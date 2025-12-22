const lines = [
  "You got this!",
  "XP!!!",
  "Keep going!",
  "Feed me!?",
  "I was going to give hints but got lazy...",
  "I'm yours!",
  "Keep playing!",
  "YAHAAAA!!!",
  "ABC",
  "Random words API broke...",
  "Hello!",
  "FOOD!!!"
];

function creatureSpeak() {
  const speech = document.getElementById("creature-speech");
  const rand = lines[Math.floor(Math.random() * lines.length)];
  speech.textContent = rand;

  speech.classList.remove("hidden");

  setTimeout(() => {
    speech.classList.add("hidden");
  }, 3000);

}

let timer = null;
function loadingScreen() {
  timer = setTimeout(() => {
    const overlay = document.getElementById("loading-screen");
    if (overlay) {
      overlay.classList.remove("hidden");
    }
  }, 250);
}

window.addEventListener("pageshow", function() {
  if (timer) {
    clearTimeout(timer);
    timer = null;
  }
  const overlay = document.getElementById("loading-screen");
  if (overlay) {
    overlay.classList.add("hidden");
  }
});
