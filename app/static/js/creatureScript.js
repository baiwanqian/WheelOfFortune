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
