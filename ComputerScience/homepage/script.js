document.addEventListener("DOMContentLoaded",()=>{
    const year = document.getElementById("year");
    if(year) year.textContent = new Date().getFullYear();

    const clock = document.getElementById("clock");
    if(clock) setInterval(()=>{clock.textContent = new Date().toLocaleTimeString();},1000);

    const toggle = document.getElementById("themeToggle");
    const body = document.body;
    const saved = localStorage.getItem("theme");
    if(saved) body.setAttribute("data-theme", saved);

    if(toggle){
        toggle.addEventListener("click",()=>{
            const next = body.getAttribute("data-theme") === "dark" ? "light" : "dark";
            body.setAttribute("data-theme",next);
            localStorage.setItem("theme", next);
            toggle.textContent = next === "dark" ? "Light mode" : "Dark mode";
        });
    }



    const form = document.getElementById("contactForm");
    if(form){
        form.addEventListener("submit", (e) => {
            e.preventDefault();
            document.getElementById("formAlert").classList.remove("d-none");
            form.reset();
        });
    }
});
