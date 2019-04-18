/*<input type="text" id="a" value="5">
<script>*/
 var x = document.getElementById("a").value;
 console.log(x);


for(var i=1; i<=31; i++) {

if(i==x||i==x+7||i==x+14||i==x+21||i==x+28)
var element = document.getElementsById("day"+i);
 element .style.backgroundColor = "red";

}
/*
</script>*/