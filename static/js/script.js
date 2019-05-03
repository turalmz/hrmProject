
// var x = document.getElementById("a").value;
// console.log(x);

window.onload = function(e){

 var table = document.getElementById("result_list");

 var trs = document.querySelectorAll('#result_list tbody tr');



for(var i = 0; i < table.tBodies.length; i++) {
  var tbody =  table.tBodies[i];
  for (var j = 0; j < tbody.rows.length; j++) {
    var row = tbody.rows[j];
    console.log(row);
    for (var k = 0; k < row.cells.length; k++) {
      var cell = row.cells[k];
      if (cell.className =="field-get_weekday"){

          console.log(cell.value);
          console.log("yes");
      }
      console.log(cell);
    }
  }
}



 for(var i = 0; i < trs.length; i++) {
console.log(trs[i]);
}


}


/*
for(var i=1; i<=31; i++) {

if(i==x||i==x+7||i==x+14||i==x+21||i==x+28)
var element = document.getElementsById("day"+i);
 element .style.backgroundColor = "red";

}
*/
