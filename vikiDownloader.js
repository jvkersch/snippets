 function findVideoUrl(baseUrl) {
     var vidUrl = undefined;
    
     $.ajax({
         type: "GET",
         async: false,
         url: baseUrl,
         dataType: "html",
         success: function(data) {
             vidUrl = data.match("src=\"(.*\.mp4.*)\"")[1];
         }
     });
    
     return vidUrl;
}

function findBaseUrl() {

}
