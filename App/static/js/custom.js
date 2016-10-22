/*
Created By: Alec Waichunas
Date: 10/21/2016

Add any javascript to this file

*/

$(document).ready(function(){
    
    $('#enrollment_date').datetimepicker();
    $('#bed_date').datetimepicker();
    $('#birth_date').datetimepicker();
    
    /*http://stackoverflow.com/questions/13437446/how-to-display-selected-item-in-bootstrap-button-dropdown-title*/
    // for(var i = 1; i < 100; i++){
    //     $("#dropdown" + i).on('click', 'li a', function(){
    //         console.log("Hello world");
    //         $(this).parent().children("Button").text($(this).text()).val($(this).text());
    //     });
    // }
    
    /*Test this bit*/
    $(".dropdown-menu li a").click(function(){
        $(this).parents(".dropdown").find('.btn').html($(this).text() + ' <span class="caret"></span>');
        $(this).parents(".dropdown").find('.btn').val($(this).data('value'));
    });
    
    //EDIT SHELTER.HTML
    $("#room_input").change(function(){
        if($(this).is(":checked")){
            $("#room_rooms").removeClass("hidden")
        }else{
            $("#room_rooms").addClass("hidden")
        }
    })
    
});

