document.addEventListener("DOMContentLoaded", function() {
    const tabs = document.querySelectorAll(".tab");
    const contents = document.querySelectorAll(".content");
    const line = document.querySelector(".line");

    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            tabs.forEach(t => t.classList.remove("active"));
            contents.forEach(c => c.classList.remove("active"));

            tab.classList.add("active");
            document.getElementById(tab.dataset.tab).classList.add("active");

            // Move the line
            const activeTab = document.querySelector(".tab.active");
            line.style.width = `${activeTab.offsetWidth}px`;
            line.style.left = `${activeTab.offsetLeft}px`;
        });
    });

    // Initialize with the first tab active
    tabs[0].click();
});
