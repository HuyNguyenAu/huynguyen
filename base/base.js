/* jshint esversion: 6 */
/* jshint browser: true */
/* jslint devel: true */

(function () {
  setTheme();

  document.addEventListener('DOMContentLoaded', onDOMContentLoaded);
  /**
   * Initialise burger, navbar items, and go to top button.
   */
  function onDOMContentLoaded() {
    initBurger();
    initGoToTopButton();
    setTheme();
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

  /**
   * Set the theme based on the theme defined in the document.location.
   */
  function setTheme() {
    const elements = document.querySelectorAll(
      'html, body, nav, footer, .card, .box, h1, p, button, a, #navbar'
    );
    const theme = getTheme(document.location);

    for (let i = 0; i < elements.length; i++) {
      const element = elements[i];

      if (theme === 'light') {
        element.classList.remove(
          'has-background-dark',
          'card-shadow-white',
          'has-text-white'
        );
      } else {
        if (element.classList.contains('card') || element.classList.contains('box')) {
          element.classList.add('card-shadow-white');
        }

        element.classList.add('has-background-dark', 'has-text-white');
      }
    }
  }

  /**
   * Get the theme from the given url.
   *
   * @param String url
   *
   * @return String
   */
  function getTheme(location) {
    const url = new URL(location);

    return url.searchParams.get('theme');
  }
})();
