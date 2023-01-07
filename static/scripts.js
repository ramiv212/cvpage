console.log('why are you looking at my console ( ͡° ͜ʖ ͡°)')

function emailValidation(response) {

    if (response && response.name_validation && response.email_validation && response.message_validation) {
        document.getElementById('contact-form-container').style.display = 'none';
        document.getElementById('contact-success-message').style.display = 'flex';
        return}
    
    if (response && !response.name_validation) document.getElementById('name-validation').style.display = 'block'
    if (response && !response.email_validation) document.getElementById('email-validation').style.display = 'block'
    if (response && !response.message_validation) document.getElementById('message-validation').style.display = 'block'
}

function sendEmail(body) {
    fetch('/api/contact', {
        method:'POST',
        headers: {
            'Content-Type': 'application/json',

        },
        body: JSON.stringify(body),
    })
    .then((response) => response.json())
    .then((data) =>{
        console.log('success!!',data);
        emailValidation(data)
    })
}

function redirectToChess() {
    window.location.href = "https://www.chess.ramirovaldes.com"
}