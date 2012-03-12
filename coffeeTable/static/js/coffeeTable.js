

$(document).ready(function() {

    console.log(check_print_view);

    if (check_print_view)
        {
        $(".edit_view").hide();
        $(".img_no").hide();
        $(".empty").hide();
        $(".print_view").show();   
        }
        
    else
        {
        $(".print_view").hide();
        }

});




