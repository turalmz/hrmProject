
if (!$) {
    $ = django.jQuery;
}

$( document ).ready(function() {



$('.field-all').change(function() {

console.log($(this).prop('checked'));
console.log($(this).is(":checked"));

console.log($(this).attr("checked"));



//
//   console.log($(this));
//   console.log($(this).parent());
//   console.log($(this).parent().children());
//   console.log($(this).parent().children().children());

   if($(this).is(":checked")){


        //$(this).parent().children().children().prop('checked', false); // Checks it

        $(this).parent().children().children().each(function( index ) {
          console.log( $( this ).prop("checked") == true );
        });

   }
   else{

        //$(this).parent().children().children().prop('checked', true); // Unchecks it

   }


});

});