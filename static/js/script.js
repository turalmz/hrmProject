

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

      //console.log(cell);
      //console.log(day);


      if(day==7-sunday){

        cell.style.backgroundColor = "#79aec8";
      }else if(day==(7-sunday+7)){

        cell.style.backgroundColor = "#79aec8";
      }else if(day==(7-sunday+14)){

        cell.style.backgroundColor = "#79aec8";
      }else if(day==(7-sunday+21)){

        cell.style.backgroundColor = "#79aec8";
      }else if(day==(7-sunday+28)){

        cell.style.backgroundColor = "#79aec8";
      }

    }
}





}


/*
    window.onload = function() {
        var anchors = document.getElementsByClassName('field-all');
        for(var i = 0; i < anchors.length; i++) {

            var anchor = anchors[i];
            console.log(anchor);

            console.log(anchor.childNodes);

            anchor.onclick = function() {
                console.log("got you");
                //var val = !anchor.checked;
                var c = anchor.parentNode.childNodes;



                    for (var i1 = 0; i1 < c.length; i1++) {
                    var p = c[i1];
                    if( p.className !='field-all'){

                        console.log(p);
                         //p.checked = anchor.checked;

                        var pch = p.childNodes;
                        console.log(pch);
                         //for (var p1 in p.childNodes)
                         for (var i2 = 0; i2 < pch.length; i2++) {
                            var p1 = pch[i2];
                        console.log(p1);
                         //p.checked = anchor.checked;
                         //p1.checked = true;

                         p1.checked = !anchor.checked;




                        }

                    }
                    }

            }
        }
    }

*/
