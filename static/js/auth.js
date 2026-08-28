/* =========================================================
   FOREX JOURNAL — AUTH JAVASCRIPT
   Login + Register
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    /* =====================================================
       LUCIDE ICONS
       ===================================================== */

    if (window.lucide) {
        lucide.createIcons();
    }


    /* =====================================================
       PASSWORD TOGGLE FUNCTION
       ===================================================== */

    function setupPasswordToggle(inputId, buttonId) {

        const input = document.getElementById(inputId);
        const button = document.getElementById(buttonId);

        if (!input || !button) {
            return;
        }

        button.addEventListener("click", function () {

            const isPassword =
                input.type === "password";

            input.type =
                isPassword ? "text" : "password";

            this.setAttribute(
                "aria-label",
                isPassword
                    ? "Hide password"
                    : "Show password"
            );

            const icon = this.querySelector("svg");

            if (icon) {

                icon.setAttribute(
                    "data-lucide",
                    isPassword
                        ? "eye-off"
                        : "eye"
                );

            }

            if (window.lucide) {
                lucide.createIcons();
            }

        });

    }


    /* Login password */

    setupPasswordToggle(
        "password",
        "passwordToggle"
    );


    /* Register confirm password */

    setupPasswordToggle(
        "confirm_password",
        "confirmPasswordToggle"
    );


    /* =====================================================
       INPUT FOCUS EFFECT
       ===================================================== */

    const inputs =
        document.querySelectorAll(
            ".input-wrapper input"
        );


    inputs.forEach(function (input) {

        input.addEventListener(
            "focus",
            function () {

                this.parentElement.classList.add(
                    "input-focused"
                );

            }
        );


        input.addEventListener(
            "blur",
            function () {

                this.parentElement.classList.remove(
                    "input-focused"
                );

            }
        );

    });


    /* =====================================================
       LOGIN FORM
       ===================================================== */

    const loginForm =
        document.getElementById("loginForm");

    const loginButton =
        document.getElementById("loginButton");


    if (loginForm && loginButton) {

        loginForm.addEventListener(
            "submit",
            function (event) {

                const email =
                    document.getElementById("email");

                const password =
                    document.getElementById("password");


                if (
                    !email ||
                    !password ||
                    !email.value.trim() ||
                    !password.value.trim()
                ) {

                    event.preventDefault();

                    return;
                }


                /* Email validation */

                const emailPattern =
                    /^[^\s@]+@[^\s@]+\.[^\s@]+$/;


                if (
                    !emailPattern.test(
                        email.value.trim()
                    )
                ) {

                    event.preventDefault();

                    email.focus();

                    return;
                }


                /* Loading */

                loginButton.classList.add(
                    "loading"
                );

                loginButton.disabled = true;

            }
        );

    }


    /* =====================================================
       REGISTER FORM
       ===================================================== */

    const registerForm =
        document.getElementById("registerForm");

    const registerButton =
        document.getElementById("registerButton");


    if (registerForm && registerButton) {

        registerForm.addEventListener(
            "submit",
            function (event) {

                const name =
                    document.getElementById("name");

                const email =
                    document.getElementById("email");

                const password =
                    document.getElementById("password");

                const confirmPassword =
                    document.getElementById(
                        "confirm_password"
                    );

                const terms =
                    document.getElementById("terms");


                /* ======================================
                   NAME
                   ====================================== */

                if (
                    !name ||
                    name.value.trim().length < 2
                ) {

                    event.preventDefault();

                    if (name) {
                        name.focus();
                    }

                    return;
                }


                /* ======================================
                   EMAIL
                   ====================================== */

                const emailPattern =
                    /^[^\s@]+@[^\s@]+\.[^\s@]+$/;


                if (
                    !email ||
                    !emailPattern.test(
                        email.value.trim()
                    )
                ) {

                    event.preventDefault();

                    if (email) {
                        email.focus();
                    }

                    return;
                }


                /* ======================================
                   PASSWORD
                   ====================================== */

                if (
                    !password ||
                    password.value.length < 8
                ) {

                    event.preventDefault();

                    if (password) {
                        password.focus();
                    }

                    return;
                }


                /* ======================================
                   CONFIRM PASSWORD
                   ====================================== */

                if (
                    !confirmPassword ||
                    password.value !==
                    confirmPassword.value
                ) {

                    event.preventDefault();

                    if (confirmPassword) {
                        confirmPassword.focus();
                    }

                    showPasswordMismatch();

                    return;
                }


                /* ======================================
                   TERMS
                   ====================================== */

                if (
                    !terms ||
                    !terms.checked
                ) {

                    event.preventDefault();

                    if (terms) {
                        terms.focus();
                    }

                    return;
                }


                /* ======================================
                   LOADING
                   ====================================== */

                registerButton.classList.add(
                    "loading"
                );

                registerButton.disabled = true;

            }
        );

    }


    /* =====================================================
       PASSWORD STRENGTH
       ===================================================== */

    const passwordInput =
        document.getElementById("password");

    const passwordStrength =
        document.getElementById(
            "passwordStrength"
        );

    const strengthText =
        document.getElementById(
            "strengthText"
        );


    if (
        passwordInput &&
        passwordStrength &&
        strengthText
    ) {

        passwordInput.addEventListener(
            "input",
            function () {

                const password =
                    this.value;


                passwordStrength.className =
                    "password-strength";


                if (!password) {

                    strengthText.textContent =
                        "Use 8+ characters";

                    return;
                }


                let score = 0;


                /* Length */

                if (password.length >= 8) {
                    score++;
                }

                if (password.length >= 12) {
                    score++;
                }


                /* Lowercase */

                if (/[a-z]/.test(password)) {
                    score++;
                }


                /* Uppercase */

                if (/[A-Z]/.test(password)) {
                    score++;
                }


                /* Number / Symbol */

                if (
                    /[0-9]/.test(password) ||
                    /[^A-Za-z0-9]/.test(password)
                ) {
                    score++;
                }


                /* Result */

                if (score <= 2) {

                    passwordStrength.classList.add(
                        "weak"
                    );

                    strengthText.textContent =
                        "Weak password";

                } else if (score === 3) {

                    passwordStrength.classList.add(
                        "medium"
                    );

                    strengthText.textContent =
                        "Medium password";

                } else if (score === 4) {

                    passwordStrength.classList.add(
                        "good"
                    );

                    strengthText.textContent =
                        "Good password";

                } else {

                    passwordStrength.classList.add(
                        "strong"
                    );

                    strengthText.textContent =
                        "Strong password";

                }

            }
        );

    }


    /* =====================================================
       PASSWORD MATCH
       ===================================================== */

    const confirmPassword =
        document.getElementById(
            "confirm_password"
        );

    const passwordMatch =
        document.getElementById(
            "passwordMatch"
        );


    function checkPasswordMatch() {

        if (
            !confirmPassword ||
            !passwordMatch ||
            !passwordInput
        ) {
            return;
        }


        if (!confirmPassword.value) {

            passwordMatch.textContent = "";

            confirmPassword
                .parentElement
                .classList.remove(
                    "input-valid",
                    "input-error"
                );

            return;
        }


        if (
            passwordInput.value ===
            confirmPassword.value
        ) {

            passwordMatch.textContent =
                "✓ Passwords match";

            passwordMatch.className =
                "password-match match";


            confirmPassword
                .parentElement
                .classList.add(
                    "input-valid"
                );

            confirmPassword
                .parentElement
                .classList.remove(
                    "input-error"
                );

        } else {

            passwordMatch.textContent =
                "✕ Passwords do not match";

            passwordMatch.className =
                "password-match no-match";


            confirmPassword
                .parentElement
                .classList.add(
                    "input-error"
                );

            confirmPassword
                .parentElement
                .classList.remove(
                    "input-valid"
                );

        }

    }


    if (passwordInput) {

        passwordInput.addEventListener(
            "input",
            checkPasswordMatch
        );

    }


    if (confirmPassword) {

        confirmPassword.addEventListener(
            "input",
            checkPasswordMatch
        );

    }


    /* =====================================================
       MISMATCH HELPER
       ===================================================== */

    function showPasswordMismatch() {

        if (
            !passwordMatch ||
            !confirmPassword
        ) {
            return;
        }


        passwordMatch.textContent =
            "✕ Passwords do not match";

        passwordMatch.className =
            "password-match no-match";


        confirmPassword
            .parentElement
            .classList.add(
                "input-error"
            );

    }


    /* =====================================================
       FLASH MESSAGE AUTO HIDE
       ===================================================== */

    const flashMessages =
        document.querySelectorAll(
            ".flash-message"
        );


    flashMessages.forEach(function (message) {

        setTimeout(function () {

            message.style.opacity = "0";

            message.style.transform =
                "translateY(-8px)";

            message.style.transition =
                "all 0.35s ease";


            setTimeout(function () {

                message.remove();

            }, 350);

        }, 4500);

    });


    /* =====================================================
       BUTTON RIPPLE
       ===================================================== */

    const buttons =
        document.querySelectorAll(
            ".auth-button"
        );


    buttons.forEach(function (button) {

        button.addEventListener(
            "click",
            function (event) {

                const ripple =
                    document.createElement(
                        "span"
                    );


                const rect =
                    this.getBoundingClientRect();


                const size =
                    Math.max(
                        rect.width,
                        rect.height
                    );


                ripple.style.width =
                    `${size}px`;

                ripple.style.height =
                    `${size}px`;

                ripple.style.position =
                    "absolute";

                ripple.style.borderRadius =
                    "50%";

                ripple.style.background =
                    "rgba(255,255,255,0.15)";

                ripple.style.pointerEvents =
                    "none";

                ripple.style.left =
                    `${event.clientX - rect.left - size / 2}px`;

                ripple.style.top =
                    `${event.clientY - rect.top - size / 2}px`;

                ripple.style.transform =
                    "scale(0)";

                ripple.style.animation =
                    "authRipple 0.6s ease-out";


                this.appendChild(ripple);


                setTimeout(function () {

                    ripple.remove();

                }, 650);

            }
        );

    });


    /* =====================================================
       PAGE READY
       ===================================================== */

    document.body.classList.add(
        "auth-page-ready"
    );

});