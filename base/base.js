/* jshint esversion: 6 */
/* jshint browser: true */
/* jslint devel: true */

(function () {
  if (!getTheme(document.location)) {
    document.location.search = 'theme=light';
  } else {
    setThemeButtonText();
    setTheme();
  }

  document.addEventListener('DOMContentLoaded', onDOMContentLoaded);
  document.getElementById('theme').addEventListener('click', onThemeButtonClicked);
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

  /**
   * Switch theme between light and dark when clicked.
   * Theme set to light when error occurs.
   */
  function onThemeButtonClicked() {
    let theme = 'theme=light';

    if (getTheme(document.location) === 'light') {
      theme = 'theme=dark';
    }

    document.location.search = theme;

    setTheme();
  }

  /**
   * Set the theme based on the theme defined in the document.location.
   */
  function setTheme() {
    const elements = document.querySelectorAll(
      'html, body, nav, footer, .card, .box, h1, p, button, a, #navbar, .code'
    );
    const theme = getTheme(document.location);

    for (let i = 0; i < elements.length; i++) {
      const element = elements[i];

      if (theme === 'light') {
        element.classList.remove(
          'has-background-black',
          'card-shadow-white',
          'has-text-white'
        );

        if (element.classList.contains('code')) {
          element.classList.add(
            'has-background-light',
          );
        }
      } else {
        if (element.classList.contains('card') || element.classList.contains('box')) {
          element.classList.add('card-shadow-white');
        }

        if (element.classList.contains('code')) {
          element.classList.remove(
            'has-background-light',
          );

          element.classList.add(
            'has-background-dark',
            'has-text-white'
          );
        } else {
          element.classList.add('has-background-black', 'has-text-white');
        }

        const parent = element.parentElement;

        if (parent) {
          if (parent.classList.contains('code')) {
            element.classList.add(
              'has-background-dark',
            );
          }
        }
      }

      if (element.tagName === 'A') {
        const link = element.getAttribute('href');

        if (link && !link.startsWith("https://")) {
          element.setAttribute('href', `${link}?theme=${theme}`)
        }
      }
    }

    setThemeButtonText();
  }

  /**
   * Change the theme button text to current theme.
   */
  function setThemeButtonText() {
    let themeText = 'Dark';

    if (getTheme(document.location) === 'dark') {
      themeText = 'Light';
    }

    document.getElementById('theme').innerText = `${themeText} Mode`;
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
