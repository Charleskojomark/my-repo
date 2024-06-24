document.addEventListener("DOMContentLoaded", function() {
    const urlParams = new URLSearchParams(window.location.search);
    const activeCategory = urlParams.get('category') || localStorage.getItem('activeCategory');
    if (activeCategory) {
        const activeCard = document.querySelector(`.card[data-category="${activeCategory}"]`);
        if (activeCard) {
            activeCard.classList.add('active');
            const subCategoryContent = activeCard.querySelector('.sub-category').innerHTML;
            const subCategoryDisplay = document.querySelector('.sub-category-content');
            subCategoryDisplay.innerHTML = subCategoryContent;
            subCategoryDisplay.style.display = 'flex';
            localStorage.setItem('activeCategory', activeCategory);  // Store active category in localStorage
        }
    } else {
        const firstCard = document.querySelector('.card');
        if (firstCard) {
            firstCard.classList.add('active');
            const subCategoryContent = firstCard.querySelector('.sub-category').innerHTML;
            const subCategoryDisplay = document.querySelector('.sub-category-content');
            subCategoryDisplay.innerHTML = subCategoryContent;
            subCategoryDisplay.style.display = 'flex';
        }
    }
});

function showSubCategory(card) {
    const cards = document.querySelectorAll('.card');
    cards.forEach(c => c.classList.remove('active'));

    card.classList.add('active');
    const subCategoryContent = card.querySelector('.sub-category').innerHTML;
    const subCategoryDisplay = document.querySelector('.sub-category-content');
    subCategoryDisplay.innerHTML = subCategoryContent;
    subCategoryDisplay.style.display = 'flex';

    const activeCategory = card.getAttribute('data-category');
    localStorage.setItem('activeCategory', activeCategory);
}
