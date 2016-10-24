/*
Created By: Alec Waichunas
Date: 10/21/2016

Add any javascript to this file

*/

$(document).ready(function(){
    
    $('#enrollment_date').datetimepicker({
        format: 'YYYY-MM-DD'
    });
    $('#bed_date').datetimepicker({
        format: 'YYYY-MM-DD'
    });
    $('#birth_date').datetimepicker({
        format: 'YYYY-MM-DD'
    });
    

    // Drop Downs
    $(".dropdown-menu li a").click(function(){
        $(this).parents(".dropdown").find('.btn').html($(this).text() + ' <span class="caret"></span>');
        $(this).parents(".dropdown").find('.btn').val($(this).data('value'));
    });
    
    // EDIT SHELTER.HTML
    $("#room_input").change(function(){
        if($(this).is(":checked")){
            $("#room_rooms").removeClass("hidden")
        }else{
            $("#room_rooms").addClass("hidden")
        }
    })
    
    $("#food_input").change(function(){
        if($(this).is(":checked")){
            $("#food_foods").removeClass("hidden")
        }else{
            $("#food_foods").addClass("hidden")
        }
    })
    
});

