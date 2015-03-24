$(function () {
    $('.company-delete-anchor').click( function(ev){
        ev.preventDefault();
        var $self=$(this);
        // Update name of the member in the dialog
        $( "#companyname" ).html($self.parent().siblings( '.company-name' ).children().html());
        // Show confirmation box
        $( "#confirm-company-delete" ).dialog({
            resizable:false,
            height:200,
            width:600,
            modal: true,
            buttons: {
                "Delete": function() {
                    document.location = $self.attr('href');
                },
                Cancel: function() {
                    $( this ).dialog( "close" );
                }
            }
        });
    });
});
