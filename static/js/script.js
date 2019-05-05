

function isSunday(day, sunday) {

 if((day==sunday) || (day==sunday+7)||(day=sunday+14)||(sunday+21)){
    return True;
 }
  return False;
}


window.onload = function(e){

 var table = document.getElementById("result_list");


 var trs = document.querySelectorAll('#result_list tbody tr');





 for(var i = 0; i < trs.length; i++) {

    var row = trs[i];

     var sunday=0;


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

    }
}


}


