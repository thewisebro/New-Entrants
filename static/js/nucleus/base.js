function open_login_dialog(){
  dialog_iframe({
    name: 'login_dialog',
    title: 'Sign In',
    width: 400,
    height: 200,
    src: '/login_dialog/?next=/close_dialog/login_dialog/',
    close: function(){
      load_pagelet('header');
    }
  });
}
