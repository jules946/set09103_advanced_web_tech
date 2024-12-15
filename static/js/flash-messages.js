document.addEventListener('DOMContentLoaded', () => {
    const flashMessages = document.querySelectorAll('.flash-message');

    flashMessages.forEach(message => {
        setTimeout(() => {
            message.classList.add('fade-out');
        }, 1000);


        setTimeout(() => {
            message.remove();
        }, 5000);
    });
});
