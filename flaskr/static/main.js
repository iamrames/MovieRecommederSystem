/* Scripts for css grid dashboard */

$(document).ready(() => {
    addResizeListeners();
    setSidenavListeners();
    setUserDropdownListener();
    setMenuClickListener();
    setSidenavCloseListener();
});

// Set constants and grab needed elements
const sidenavEl = $('.sidenav');
const gridEl = $('.grid');
const SIDENAV_ACTIVE_CLASS = 'sidenav--active';
const GRID_NO_SCROLL_CLASS = 'grid--noscroll';

function toggleClass(el, className) {
    if (el.hasClass(className)) {
        el.removeClass(className);
    } else {
        el.addClass(className);
    }
}

// User avatar dropdown functionality
function setUserDropdownListener() {
    const userAvatar = $('.header__avatar');

    userAvatar.on('click', function (e) {
        const dropdown = $(this).children('.dropdown');
        toggleClass(dropdown, 'dropdown--active');
    });
}

// Sidenav list sliding functionality
function setSidenavListeners() {
    const subHeadings = $('.navList__subheading');
    console.log('subHeadings: ', subHeadings);
    const SUBHEADING_OPEN_CLASS = 'navList__subheading--open';
    const SUBLIST_HIDDEN_CLASS = 'subList--hidden';

    subHeadings.each((i, subHeadingEl) => {
        $(subHeadingEl).on('click', (e) => {
            const subListEl = $(subHeadingEl).siblings();

            // Add/remove selected styles to list category heading
            if (subHeadingEl) {
                toggleClass($(subHeadingEl), SUBHEADING_OPEN_CLASS);
            }

            // Reveal/hide the sublist
            if (subListEl && subListEl.length === 1) {
                toggleClass($(subListEl), SUBLIST_HIDDEN_CLASS);
            }
        });
    });
}


function toggleClass(el, className) {
    if (el.hasClass(className)) {
        el.removeClass(className);
    } else {
        el.addClass(className);
    }
}

// If user opens the menu and then expands the viewport from mobile size without closing the menu,
// make sure scrolling is enabled again and that sidenav active class is removed
function addResizeListeners() {
    $(window).resize(function (e) {
        const width = window.innerWidth;
        console.log('width: ', width);

        if (width > 750) {
            sidenavEl.removeClass(SIDENAV_ACTIVE_CLASS);
            gridEl.removeClass(GRID_NO_SCROLL_CLASS);
        }
    });
}

// Menu open sidenav icon, shown only on mobile
function setMenuClickListener() {
    $('.header__menu').on('click', function (e) {
        console.log('clicked menu icon');
        toggleClass(sidenavEl, SIDENAV_ACTIVE_CLASS);
        toggleClass(gridEl, GRID_NO_SCROLL_CLASS);
    });
}


// Sidenav close icon
function setSidenavCloseListener() {
    $('.sidenav__brand-close').on('click', function (e) {
        toggleClass(sidenavEl, SIDENAV_ACTIVE_CLASS);
        toggleClass(gridEl, GRID_NO_SCROLL_CLASS);
    });
}


//initial setup
// https://gist.github.com/prof3ssorSt3v3/29e623d441e8174ffaef17741a1bba14
// document.addEventListener('DOMContentLoaded', function(){
//     let stars = document.querySelectorAll('.star');
//     stars.forEach(function(star){
//         star.addEventListener('click', setRating); 
//     });

//     let rating = parseInt(document.querySelector('.stars').getAttribute('data-rating'));
//     let target = stars[rating - 1];
//     target.dispatchEvent(new MouseEvent('click'));
// });

function setRating(ev) {
    let span = ev.currentTarget;
    let stars = document.querySelectorAll('.star');
    let match = false;
    let num = 0;
    stars.forEach(function (star, index) {
        if (match) {
            star.classList.remove('rated');
        } else {
            star.classList.add('rated');
        }
        //are we currently looking at the span that was clicked
        if (star === span) {
            match = true;
            num = index + 1;
        }
    });
    document.querySelector('.stars').setAttribute('data-rating', num);
}
