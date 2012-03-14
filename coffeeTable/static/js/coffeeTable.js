

$(document).ready(function() {

    // Workaround, because checking Django variables wouldn't work
    if ($("#print_view").length > 0){
        $(".edit_view").hide();
        $(".img_no").hide();
        $(".empty").hide();
        $(".print_view").show();   
    }else{ 
        $(".print_view").hide();
    }
        
    // Another workaround. Silly javascript didn't want to play nice.
    if ($("#page_no").text() == 1)
        {
        $(".inside_page").hide();
        }


    if (!tried_to_edit)
        {
        $(".tried_to_edit").hide();
        }
    
});





