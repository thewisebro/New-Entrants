ajaxify = function (bundle, $errorMsgDiv) {
    var dataType = (bundle.dataType !== undefined) ? bundle.dataType : 'json';
    var async = (bundle.async != undefined) ? bundle.async : true;
    var cache = (bundle.cache != undefined) ? bundle.cache : true;
    var type = (bundle.type != undefined) ? bundle.type : 'POST';
    $.ajax({
        type: type,
        url: bundle.url,
        data: bundle.data,
        dataType: dataType,
        async: async,
        cache: cache,
        beforeSend: function (data) {
            if (typeof bundle.beforeSend === 'function') {
                bundle.beforeSend(data);
            }			
        },
        
        success: function (data) {
            /*alert('successFunc');
            alert(data.status);*/
            if (typeof bundle.success === 'function') {
              bundle.success(data);
            }
        },
        error: function (data) {
            //alert('errorFunc');
            if (typeof bundle.error === 'function') {
                bundle.error(data);
            }
            else {
                var response = data;
                if($errorMsgDiv != null)
                    $errorMsgDiv.html('There was some error in the ajax request.');
                console.log('error details : ' + response.status);
            }
        }
    });    	
};
