
const element = document.getElementById('bttm');
const element2 = document.getElementById('tp');
const form = document.getElementById('htc');
const button = form.querySelector('input[type="submit"]');

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
            form.submit();
            moving = false;
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
