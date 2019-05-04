
// var x = document.getElementById("a").value;
// console.log(x);


function isSunday(day, sunday) {

 if((day==sunday) || (day==sunday+7)||(day=sunday+14)||(sunday+21)){
    return True;
 }
  return False;
}


window.onload = function(e){

 var table = document.getElementById("result_list");


 var trs = document.querySelectorAll('#result_list tbody tr');



// for(var i = 0; i < table.tBodies.length; i++) {
//   var tbody =  table.tBodies[i];
//   for (var j = 0; j < tbody.rows.length; j++) {
//     var row = tbody.rows[j];
//     console.log(row);
//     for (var k = 0; k < row.cells.length; k++) {
//       var cell = row.cells[k];
//
//       if (cell.className =="field-get_weekday"){
//
//           console.log(cell.value);
//           console.log("yes");
//       }
//       console.log(cell);
//     }
//   }
// }



 for(var i = 0; i < trs.length; i++) {
//console.log(trs[i].className);

    var row = trs[i];

     var sunday=0;
     var sunday1=7;
     var sunday2=14;
     var sunday3=21;

    for (var k = 0; k < row.cells.length; k++) {
      var cell = row.cells[k];
      if (cell.className =="field-get_weekday"){
          sunday = Number(cell.innerText);
          console.log("sunday:");
          console.log(sunday);
      }
      var classname = cell.className;

      var num = Number(classname.replace(/[^0-9]/g,''));
      var day = num;

      console.log(cell);
      console.log(day);


      if(day==sunday){

        cell.style.backgroundColor = "#79aec8";
      }else if(day==(sunday+7)){

        cell.style.backgroundColor = "#79aec8";
      }else if(day==(sunday+14)){

        cell.style.backgroundColor = "#79aec8";
      }else if(day==(sunday+21)){

        cell.style.backgroundColor = "#79aec8";
      }else if(day==(sunday+28)){

        cell.style.backgroundColor = "#79aec8";
      }

      //console.log(numb);
    }
}


}




/*
for(var i=1; i<=31; i++) {

if(i==x||i==x+7||i==x+14||i==x+21||i==x+28)
var element = document.getElementsById("day"+i);
 element .style.backgroundColor = "red";

}
*/
