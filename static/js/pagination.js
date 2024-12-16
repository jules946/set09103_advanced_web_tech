// pagination.js

class ResultsPagination {
    constructor() {
        // DOM elements
        this.prevButton = document.getElementById('prev-page');
        this.nextButton = document.getElementById('next-page');
        this.currentPageSpan = document.getElementById('current-page');

        // pagination state
        this.currentPage = 1;
        this.resultsPerPage = 10;
        this.totalResults = document.querySelectorAll('.result-row').length;
        this.totalPages = Math.ceil(this.totalResults / this.resultsPerPage);

        // bind event listeners
        this.initializeEventListeners();

        // show initial page
        this.showPage(1);
    }

    initializeEventListeners() {
        this.prevButton.addEventListener('click', () => this.handlePrevClick());
        this.nextButton.addEventListener('click', () => this.handleNextClick());
    }

    showPage(pageNum) {
        // hide all rows
        const rows = document.querySelectorAll('.result-row');
        rows.forEach(row => {
            row.style.display = 'none';
        });

        // calculate range for current page
        const startIdx = (pageNum - 1) * this.resultsPerPage;
        const endIdx = Math.min(startIdx + this.resultsPerPage, this.totalResults);

        // show rows for current page
        for (let i = startIdx; i < endIdx; i++) {
            rows[i].style.display = 'grid';
        }

        // update UI state
        this.updateUIState(pageNum);
    }

    updateUIState(pageNum) {
        // update button states
        this.prevButton.disabled = pageNum === 1;
        this.nextButton.disabled = pageNum === this.totalPages;

        // update page counter
        this.currentPageSpan.textContent = pageNum;
    }

    handlePrevClick() {
        if (this.currentPage > 1) {
            this.currentPage--;
            this.showPage(this.currentPage);
        }
    }

    handleNextClick() {
        if (this.currentPage < this.totalPages) {
            this.currentPage++;
            this.showPage(this.currentPage);
        }
    }
}

// initialize pagination when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('.result-row')) {
        new ResultsPagination();
    }
});