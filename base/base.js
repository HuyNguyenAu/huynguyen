/* jshint esversion: 6 */
/* jshint browser: true */
/* jslint devel: true */

(function () {
  document.addEventListener('DOMContentLoaded', onDOMContentLoaded);
  /**
   * Initialise burger, navbar items, and go to top button.
   */
  function onDOMContentLoaded() {
    initBurger();
    initGoToTopButton();
  }

  /**
   * Add click listener tonavbar-burger button.
   */
  function initBurger() {
    document.querySelector('.navbar-burger').addEventListener('click', function (e) {
      e.currentTarget.classList.toggle('is-active');
      document
        .getElementById(e.currentTarget.dataset.target)
        .classList.toggle('is-active');
    });
  }

  /**
   * Add click listener to go-to-top button. If an error occurs try to remove the go-to-top button.
   */
  function initGoToTopButton() {
    document
      .getElementById('go-to-top')
      .addEventListener('click', function () {
        /* There is a bug where if the vertical scroll position is at 0 or scrollMaxY,
        the returned value is mostly scrollMaxY. To prevent this, we just need to set either at
        1 or window.scrollMaxY - 1. */
        window.scrollTo(0, 1);
      });
  }
})();
