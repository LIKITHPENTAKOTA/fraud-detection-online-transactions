document.addEventListener("DOMContentLoaded", function () {

    /* =========================
       THEME HANDLING
    ==========================*/

    if (!localStorage.getItem("theme")) {
        localStorage.setItem("theme", "light");
    }

    document.body.classList.add(localStorage.getItem("theme"));

    const toggle = document.querySelector(".theme-toggle");
    const icon = document.getElementById("theme-icon");

    function updateIcon() {
        if (document.body.classList.contains("dark")) {
            icon.classList.remove("bi-moon-stars-fill");
            icon.classList.add("bi-sun-fill");
        } else {
            icon.classList.remove("bi-sun-fill");
            icon.classList.add("bi-moon-stars-fill");
        }
    }

    updateIcon();

    toggle.addEventListener("click", function () {

        document.body.classList.toggle("dark");
        document.body.classList.toggle("light");

        let currentTheme = document.body.classList.contains("dark") ? "dark" : "light";
        localStorage.setItem("theme", currentTheme);

        updateIcon();
    });

    /* =========================
       FILL SAMPLE FRAUD DATA
    ==========================*/

    const fillBtn = document.getElementById("fill-sample");

    if (fillBtn) {
        fillBtn.addEventListener("click", function () {

            const fraudSample = [
                -2.303349568, 1.75924746, -0.359744743, 2.330243051, -0.821628328,
                -0.075787571, 0.562319782, -0.399146578, -0.238253368, -1.525411627,
                2.032912158, -6.560124295, 0.022937323, -1.470101536, -0.698826069,
                -2.282193829, -4.781830856, -2.615664945, -1.334441067, -0.430021867,
                -0.294166318, -0.932391057, 0.172726296, -0.087329538, -0.156114265,
                -0.542627889, 0.039565989, -0.153028797, 239.93
            ];

            const inputs = document.querySelectorAll(".modern-input");

            inputs.forEach((input, index) => {
                input.value = fraudSample[index];
            });
        });
    }

});
