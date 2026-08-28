document.addEventListener(
    "DOMContentLoaded",
    function () {

        const elements =
            document.querySelectorAll(
                ".stat-card, .auth-card, .hero-content"
            );

        elements.forEach(
            function (element, index) {

                element.style.animationDelay =
                    `${index * 0.08}s`;

            }
        );

    }
);