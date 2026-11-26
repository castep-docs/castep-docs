function filter_table() {
  var search = document.getElementById("search").value.toUpperCase();
  var table = document.getElementsByTagName("table")[0];
  for (var row of table.getElementsByTagName("tr")) {
    var cols = row.getElementsByTagName("td");
    if (cols.length == 0) continue;
    var text = [0, 1, 3].map(x => cols[x].textContent || cols[x].innerText).join("");
    if (text.toUpperCase().indexOf(search) > -1) {
      row.style.display = "";
    } else {
      row.style.display = "none";
    }
  }
}
