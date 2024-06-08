// services.js
document.addEventListener("DOMContentLoaded", function() {
    // Check if there is a category stored in local storage
    const activeCategory = localStorage.getItem('activeCategory');
    if (activeCategory) {
        const activeCard = document.querySelector(`.card[data-category="${activeCategory}"]`);
        if (activeCard) {
            activeCard.classList.add('active');
            const subCategoryContent = activeCard.querySelector('.sub-category').innerHTML;
            const subCategoryDisplay = document.querySelector('.sub-category-content');
            subCategoryDisplay.innerHTML = subCategoryContent;
            subCategoryDisplay.style.display = 'flex';
        }
    } else {
        // If no category is stored, make the first card active
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

    // Store the active category in local storage
    const activeCategory = card.getAttribute('data-category');
    localStorage.setItem('activeCategory', activeCategory);
}
