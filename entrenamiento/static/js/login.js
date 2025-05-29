const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const signUpMobileButton = document.getElementById('signUpMobile');
const signInMobileButton = document.getElementById('signInMobile');
const container = document.getElementById('container');

function toggleSignUp() {
    container.classList.add("right-panel-active");
}

function toggleSignIn() {
    container.classList.remove("right-panel-active");
}

// Event listeners para desktop
signUpButton?.addEventListener('click', toggleSignUp);
signInButton?.addEventListener('click', toggleSignIn);

// Event listeners para móvil
signUpMobileButton?.addEventListener('click', toggleSignUp);
signInMobileButton?.addEventListener('click', toggleSignIn); 