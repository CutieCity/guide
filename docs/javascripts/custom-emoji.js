document$.subscribe(function () {
  if (window.location.href.includes("/custom-emoji/")) {
    for (const [buttonId, callback] of [
      ["#expand-categories", () => onCategoryButtonClick(true, "expanded")],
      ["#collapse-categories", () => onCategoryButtonClick(false, "collapsed")],
      ["#enable-animations", (button) => onAnimateButtonClick(button, "first")],
      ["#pause-animations", (button) => onAnimateButtonClick(button, "last")],
    ]) {
      enableButtonAction(buttonId, callback);
    }

    if (!document.querySelector(".tabbed-set > input:first-child").checked) {
      document
        .querySelectorAll("[id^=animations-label] strong")
        .forEach((label) => (label.textContent = "paused"));
      document.querySelector("#enable-animations").classList.remove("disabled");
      document.querySelector("#pause-animations").classList.add("disabled");
    }

    document.querySelector(".grid.two-columns").classList.add("loaded");

    document
      .querySelectorAll("[href$='#emoji-categories'] + nav .md-nav__link")
      .forEach(enableCategorySmoothScroll);

    document.querySelectorAll(".category").forEach(enableCategoryListener);
    document.querySelectorAll(".grid li").forEach(enableCopyToClipboard);
  }
});

function onCategoryButtonClick(shouldOpenAll, alertLabel) {
  document
    .querySelectorAll(".category")
    .forEach((detailsElement) => (detailsElement.open = shouldOpenAll));
  alert$.next(`All categories ${alertLabel}.`);
}

function onAnimateButtonClick(clickedButtonElement, tabPosition) {
  const statusText = `${clickedButtonElement.id.match(/^[a-z]+/)}d`;
  document.querySelector(`.tabbed-labels label:${tabPosition}-child`).click();

  document
    .querySelectorAll(".md-button[id$=-animations]")
    .forEach((buttonElement) => {
      if (buttonElement.id === clickedButtonElement.id) {
        buttonElement.classList.add("disabled");
      } else {
        buttonElement.classList.remove("disabled");
      }
    });
  document
    .querySelectorAll("[id^=animations-label] strong")
    .forEach((label) => (label.textContent = statusText));

  alert$.next(`Animations ${clickedButtonElement.id.match(/^[a-z]+/)}d.`);
}

function enableButtonAction(buttonId, callback) {
  const buttonElement = document.querySelector(buttonId);
  buttonElement.addEventListener("click", () => {
    if (!buttonElement.classList.contains("disabled")) {
      callback(buttonElement);
    }
  });
}

function enableCategorySmoothScroll(linkElement) {
  const headerId = linkElement.href.match(/#[a-z-]+$/);
  const detailsElement = document.querySelector(headerId).parentNode;
  const moreOffset = detailsElement.querySelector("summary").offsetHeight * 1.5;

  linkElement.addEventListener("click", (clickEvent) => {
    clickEvent.preventDefault();
    document
      .querySelectorAll(".category")
      .forEach((element) => (element.open = element === detailsElement));
    smoothScrollTo(detailsElement.offsetTop - moreOffset, linkElement.href);
  });
}

function enableCategoryListener(detailsElement) {
  const expandButton = document.querySelector("#expand-categories");
  const collapseButton = document.querySelector("#collapse-categories");
  const categoryLabels = document.querySelectorAll("[id^=categories-label]");
  const categoryCount = document.querySelectorAll(".category").length;

  const updateButton = (buttonElement, currentCount, disableCount) => {
    if (currentCount === disableCount) {
      buttonElement.classList.add("disabled");
    } else {
      buttonElement.classList.remove("disabled");
    }
  };

  detailsElement.addEventListener("toggle", () => {
    let categoriesOpen = document.querySelectorAll(".category[open]").length;

    updateButton(collapseButton, categoriesOpen, 0);
    updateButton(expandButton, categoriesOpen, categoryCount);

    categoryLabels.forEach((label) => {
      label.querySelector("strong").textContent = categoriesOpen.toString();
    });
  });
}

function enableCopyToClipboard(cardElement) {
  cardElement.addEventListener("click", () => {
    copyToClipboard(cardElement.innerText);
  });
}
