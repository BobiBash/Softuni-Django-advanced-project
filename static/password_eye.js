function PasswordToggle (inputID, buttonID, iconID) {
    const input = document.getElementById(inputID);
    const button = document.getElementById(buttonID);
    const icon = document.getElementById(iconID);

    if (!input || !button || !icon) return;

    button.addEventListener('click', function (e) {
       const inputType = input.getAttribute('type')
            if (inputType === 'password') {
            input.type = 'text'
            icon.className = 'fa-solid fa-eye-slash'
            } else {
                input.type = 'password'
                icon.className = 'fa-solid fa-eye'
            }
    });
}

PasswordToggle('id_password1', 'TogglePassword', 'pass-icon');
PasswordToggle('id_password2', 'TogglePassword2', 'pass-icon2');
PasswordToggle('id_password', "LoginTogglePassword", 'pass-icon-login');