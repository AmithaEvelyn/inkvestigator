document.addEventListener('DOMContentLoaded', function() {
    // Add any JavaScript functionality here
    console.log('JavaScript is loaded!');
});
function togglePasswordVisibility() {
    var passwordField = document.getElementById('password');
    var eyeIcon = document.querySelector('.eye-icon');
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        eyeIcon.innerHTML = '🙈';  // Change to "hidden" icon
    } else {
        passwordField.type = 'password';
        eyeIcon.innerHTML = '🐵';  // Change to "visible" icon
    }
}