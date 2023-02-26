document$.subscribe(function () {
  const pageNav = document.querySelector(".md-nav--secondary");
  if (pageNav) {
    pageNav.querySelectorAll("a.md-nav__link").forEach(enhancePageNav);
  }
});

function copyToClipboard(textToCopy) {
  navigator.clipboard.writeText(textToCopy);
  alert$.next("Copied to clipboard.");
}

function smoothScrollTo(scrollPositionY, newWindowUrl) {
  window.scrollTo({ top: scrollPositionY, behavior: "smooth" });
  window.history.pushState({}, "", newWindowUrl);

  if (document.querySelector("[data-md-toggle='drawer']").checked) {
    document.querySelector(".md-overlay[for$='drawer']").click();
  }
}

function enhancePageNav(navLinkElement) {
  const headerId = navLinkElement.href.match(/#[a-z-]+$/);
  const headerElement = document.querySelector(headerId);
  const headerLinkElement = headerElement.querySelector("a.headerlink");

  const moreOffset = headerElement.offsetHeight * 1.9;
  const navDestination = headerLinkElement.href;

  const handleNavClick = (clickEvent) => {
    if (clickEvent.target.closest("[aria-label='Emoji Categories']") === null) {
      clickEvent.preventDefault();
      smoothScrollTo(headerElement.offsetTop - moreOffset, navDestination);
    }
  };

  headerLinkElement.addEventListener("click", (clickEvent) => {
    handleNavClick(clickEvent);
    copyToClipboard(navDestination);
  });
  navLinkElement.addEventListener("click", handleNavClick);
}
