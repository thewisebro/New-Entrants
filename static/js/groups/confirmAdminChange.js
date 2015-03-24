function confirmAdminChange(group_id,username,admin)
{
  var x = confirm ('Are you sure you want to change the admin? '+admin+' will no longer have the admin rights.')
  if (x)
  {
    window.location='/groups/'+group_id+'/'+username+'/admin_change/';
  }
}
