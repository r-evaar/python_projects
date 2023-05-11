const slider = document.querySelector('#theme-selector');
const themedElements = document.querySelectorAll('#m1, #s1');

const className = 'dark-theme';

function selectorStatusChange() {
    if (this.checked){
        themedElements.forEach((el) => el.classList.add(className));
    } else {
        themedElements.forEach((el) => el.classList.remove(className));
    }
}

slider.addEventListener('change', selectorStatusChange);
