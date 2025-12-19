
const element = document.getElementById('bttm');
const element2 = document.getElementById('tp');
const form = document.getElementById('htc');
const button = form.querySelector('input[type="submit"]');
const creature = document.getElementById("hatched-creature");

let reload = 0;
let moving = false;

form.addEventListener('submit', function(event) {

    event.preventDefault();

    if (moving) return;
    moving = true;
    button.disabled = true;

    function onDone() {
        reload++;
        if (reload === 2) {
          creature.classList.remove("hidden");
          creature.classList.add("show");

          function onCreatureDone() {
            form.submit();
            moving = false;
          }
          creature.addEventListener("transitionend", onCreatureDone, { once: true });
        }
    }

    if (element.classList.contains('hatching')) {
        element.classList.remove('hatching');
    }
    void element.offsetWidth;

    if (element2.classList.contains('hatching2')) {
        element2.classList.remove('hatching2');
    }
    void element2.offsetWidth;


    element.classList.add('hatching');
    element.addEventListener('animationend', onDone, { once: true });

    element2.classList.add('hatching2');
    element2.addEventListener('animationend', onDone, { once: true });


});
