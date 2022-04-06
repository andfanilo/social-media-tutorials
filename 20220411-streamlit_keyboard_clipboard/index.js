const streamlitDoc = window.parent.document;

buttons = Array.from(streamlitDoc.querySelectorAll('button[kind=primary]'));

const left_button = buttons.find(el => el.innerText === 'Decrement');
const right_button = buttons.find(el => el.innerText === 'Increment');
const copy_button = buttons.find(el => el.innerText === 'Copy To Clipboard');

streamlitDoc.addEventListener('keydown', function(e) {
    switch (e.key) {
        case 'ArrowLeft':
            left_button.click();
            break;
        case 'ArrowRight':
            right_button.click();
            break;
        case 'Enter':
            copy_button.click();
            break;
    }
});