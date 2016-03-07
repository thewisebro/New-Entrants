$(document).ready(function(){
      $('.delItem').click(function(){
        var flag = confirm('Do you really want to delete this item?');
        var id_type =0;
        if(flag)
        {
          id_type = $(this).attr('name');
          document.location.href = '/lostfound/delete/'+ id_type;
        }
        });
      $('.statusItemLost').click(function(){
        var flag = confirm('Do you really want to change the status of this item to "Item found"?');
        var id_type =0;
        if(flag)
        {
          id_type = $(this).attr('name');
          document.location.href = '/lostfound/status/'+ id_type;
        }
        });
      $('.statusItemFound').click(function(){
        var flag = confirm('Do you really want to change the status of this item to "Owner found"?');
        var id_type =0;
        if(flag)
        {
          id_type = $(this).attr('name');
          document.location.href = '/lostfound/status/'+ id_type;
        }
        });
    }
    );
