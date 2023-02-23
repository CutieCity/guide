document$.subscribe(function () {
  if (window.location.href.includes("/custom-emoji/")) {
    fetch("https://cutie.city/api/v1/custom_emojis")
      .then((response) => response.json())
      .then(populateTable);
  }
});

function populateTable(emojiArray) {
  const tableRoot = document.querySelector(".md-typeset__table table");
  const tableBody = tableRoot.querySelector("tbody");
  const tableHeaders = tableRoot.querySelectorAll("th");

  tableHeaders[0].setAttribute("style", "cursor: default;");
  tableHeaders[0].setAttribute("data-sort-method", "none");
  tableHeaders[1].setAttribute("data-sort-default", "");

  tableBody.querySelector("tr").remove(); // Remove the placeholder table row.
  emojiArray.forEach(addTableRow, tableBody); // Populate the actual table rows.
  new Tablesort(tableRoot); // Make the entire table sortable.
}

function addTableRow({ category, shortcode, static_url: imageUrl }) {
  const tableRow = document.createElement("tr");
  const codeElement = document.createElement("code");

  addTableCell(tableRow, createImageElement(shortcode, imageUrl));
  addTableCell(tableRow, codeElement);
  addTableCell(tableRow, category);

  codeElement.appendChild(document.createTextNode(`:${shortcode}:`));
  this.appendChild(tableRow); // Append the table row to the bound table body.
}

function addTableCell(tableRow, content) {
  const tableCell = document.createElement("td");

  tableCell.setAttribute("align", "center");
  tableCell.setAttribute("style", "vertical-align: middle;");

  tableCell.appendChild(
    typeof content === "string" ? document.createTextNode(content) : content,
  );
  tableRow.appendChild(tableCell);
}

function createImageElement(label, url) {
  const imageElement = document.createElement("img");

  imageElement.setAttribute("src", url);
  imageElement.setAttribute("alt", label);
  imageElement.setAttribute("title", label);
  imageElement.setAttribute("style", "height: 32px; width: 32px;");

  return imageElement;
}
