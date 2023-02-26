document$.subscribe(function () {
  if (window.location.href.includes("/custom-emoji/")) {
    for (const [buttonId, callback] of [
      ["#expand-categories", onExpandCategoriesClick],
      ["#collapse-categories", onCollapseCategoriesClick],
      ["#enable-animations", onEnableAnimationsClick],
      ["#pause-animations", onPauseAnimationsClick],
    ]) {
      enableButtonAction(buttonId, callback);
    }

    if (!document.querySelector(".tabbed-set > input:first-child").checked) {
      document.querySelector("#enable-animations").classList.remove("disabled");
      document.querySelector("#pause-animations").classList.add("disabled");
    }

    document.querySelectorAll(".grid li").forEach(enableCopyToClipboard);
    document.querySelectorAll(".category").forEach(enableCategoryListener);
  }
});

function enableButtonAction(buttonId, callback) {
  const buttonElement = document.querySelector(buttonId);
  buttonElement.addEventListener("click", () => {
    if (!buttonElement.classList.contains("disabled")) {
      callback(buttonElement);
    }
  });
}

function enableCopyToClipboard(cardElement) {
  cardElement.addEventListener("click", () => {
    navigator.clipboard.writeText(cardElement.innerText);
    alert$.next("Copied to clipboard.");
  });
}

function enableCategoryListener(detailsElement) {
  const expandButton = document.querySelector("#expand-categories");
  const collapseButton = document.querySelector("#collapse-categories");
  const categoryCount = document.querySelectorAll(".category").length;

  detailsElement.addEventListener("toggle", () => {
    let categoriesOpen = document.querySelectorAll(".category[open]").length;

    if (categoriesOpen === 0) {
      collapseButton.classList.add("disabled");
    } else {
      collapseButton.classList.remove("disabled");
    }

    if (categoriesOpen === categoryCount) {
      expandButton.classList.add("disabled");
    } else {
      expandButton.classList.remove("disabled");
    }
  });
}

function onExpandCategoriesClick(buttonElement) {
  document
    .querySelectorAll(".category")
    .forEach((detailsElement) => (detailsElement.open = true));
  alert$.next("All categories expanded.");
}

function onCollapseCategoriesClick(buttonElement) {
  document
    .querySelectorAll(".category")
    .forEach((detailsElement) => (detailsElement.open = false));
  alert$.next("All categories collapsed.");
}

function onEnableAnimationsClick(buttonElement) {
  document.querySelector(".tabbed-labels label:first-child").click();
  document.querySelector("#pause-animations").classList.remove("disabled");
  buttonElement.classList.add("disabled");
  alert$.next("Animations enabled.");
}

function onPauseAnimationsClick(buttonElement) {
  document.querySelector(".tabbed-labels label:last-child").click();
  document.querySelector("#enable-animations").classList.remove("disabled");
  buttonElement.classList.add("disabled");
  alert$.next("Animations paused.");
}
