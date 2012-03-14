

$(document).ready(function() {

alert("we are here!");
initiate_base();
alert("print some more.");

alert("print sth you asshole."+check_print_view);
    if (check_print_view){
            alert("and here..");
        $(".edit_view").hide();
        $(".img_no").hide();
        $(".empty").hide();
        $(".print_view").show();   
    }else{ 
        alert("in th else");
        $(".print_view").hide();
    }
        
        
    if (page_no == 1)
        {
        $(".inside_page").hide();
        }


    if (!tried_to_edit)
        {
        $(".tried_to_edit").hide();
        }
    
});





