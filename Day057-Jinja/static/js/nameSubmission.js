const contentParent = document.getElementsByClassName('appending-container')[0];

function addContainer(data, placeHolder){
    const tempHTML = document.createElement('html');
    tempHTML.innerHTML = data;

    const targetContent = tempHTML.getElementsByClassName('container')[0];

    placeHolder.innerHTML = targetContent.innerHTML;
    setTimeout(() => {
        console.log(getComputedStyle(placeHolder).height)
        placeHolder.classList.add('allocated')
        console.log(getComputedStyle(placeHolder).height)
    }, 30)
}

function addContentPlaceholder() {
    const placeHolder = document.createElement('div');
    placeHolder.classList.add('container', 'appended');
    contentParent.appendChild(placeHolder);
    setTimeout(() => {
        placeHolder.style.opacity = 1;
    }, 30);
    return placeHolder
}

function updateContent(route){
    const placeHolder = addContentPlaceholder()
    var content = fetch(route).then(r => r.text());
    content.then(data => addContainer(data, placeHolder))
}

function routeToGuess() {
    var entry = document.getElementById('name-input').value;
    if (entry !== ''){
        updateContent('/guess/'+entry);
    } else {
        alert('Please enter a name');
    }
}

