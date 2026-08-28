document.addEventListener(
    "DOMContentLoaded",
    function () {

        console.log(
            "Forex Trading Journal loaded successfully."
        );

        const inputs =
            document.querySelectorAll(
                "input"
            );

        inputs.forEach(
            function (input) {

                input.addEventListener(
                    "focus",
                    function () {

                        this.parentElement.classList.add(
                            "focused"
                        );

                    }
                );

                input.addEventListener(
                    "blur",
                    function () {

                        this.parentElement.classList.remove(
                            "focused"
                        );

                    }
                );

            }
        );

    }
);