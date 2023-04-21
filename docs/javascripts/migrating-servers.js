document$.subscribe(function () {
  if (window.location.href.includes("/migrating-servers/")) {
    const initialScrollY = window.scrollY;

    const placeholderLinks = document.querySelectorAll("[data-custom-link]");
    const placeholderText = document.querySelectorAll("[data-custom-text]");

    const accountRegex =
      /^@?(([a-z0-9_]+)@([a-z0-9]+(?:[-.][a-z0-9]+)*\.[a-z]{2,}))$/i;
    const getAccountValues = (field) => field.value.trim().match(accountRegex);

    document
      .querySelectorAll(".custom-account.input-field > input")
      .forEach((accountField, _, accountFields) => {
        accountField.addEventListener("input", () => {
          const accountValues = Array.from(accountFields, getAccountValues);
          onAccountUpdate(accountValues, placeholderLinks, placeholderText);
          accountField.focus();
        });
      });

    document
      .querySelectorAll(".tabbed-labels label:first-child")
      .forEach((tabLabel) => tabLabel.click());

    window.scrollTo(window.scrollX, initialScrollY);
  }
});

function onAccountUpdate(accountValues, placeholderLinks, placeholderText) {
  let tabPosition;

  if (!accountValues.every((valueMatch) => valueMatch !== null)) {
    tabPosition = "first";
  } else {
    tabPosition = "last";

    const substitute = getSubstituteFunction(accountValues);

    placeholderLinks.forEach((element) => {
      element.setAttribute("href", substitute(element.dataset.customLink));
    });

    placeholderText.forEach((element) => {
      element.textContent = substitute(element.dataset.customText);
    });
  }

  document.querySelector(`.tabbed-labels label:${tabPosition}-child`).click();
}

function getSubstituteFunction(accountValues) {
  const substitutionMap = {};

  ["OLD", "NEW"].forEach((keyPrefix, i) => {
    ["HANDLE", "USERNAME", "SERVER"].forEach((keySuffix, j) => {
      substitutionMap[`${keyPrefix}_${keySuffix}`] = accountValues[i][j + 1];
    });
  });

  function substitute(content) {
    for (const [key, value] of Object.entries(substitutionMap)) {
      content = content.replace(key, value);
    }
    return content;
  }

  return substitute;
}
