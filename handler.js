let host = 'https://api.northernlights.network:54321';


function startServer() {
    console.log("Start button clicked!");
    let request = JSON.stringify({
        'type': 'start',
        'process_name': 'srcds.exe',
        'startup_path':'C:\\Users\\Administrator\\Desktop\\BMRP\\Start.bat'
    });
    fetch(host, {
        method: "POST",
        headers: {
            'Content-Length': request.length
        },
        body: request}).
    then((response) => {
        if (response.ok) {
            console.log("The server was started");
            $('.col-lg-12').append('<P>The server is running!');
            $('.StatusResponse').remove()
        } else {
            console.log("The server was not started");
            $('.StatusResponse').empty().append('<P>The server was not started!');
        }
    }).catch(error => {
        $('.StatusResponse').append("<P>Error starting server!");
    });
}

$(document).ready(async function() {
   $('#StatusButton').click(() => {
       console.log("Status button clicked!");
       let request = JSON.stringify({
               'type': 'status',
               'process_name': 'srcds.exe',
               'startup_path':'C:\\Users\\Administrator\\Desktop\\BMRP\\Start.bat'});
       fetch(host, {
           method: "POST",
           body: request,
           headers: {
               'Content-Length': request.length
           }
       }).then((response) => {
          if (response.ok) {
              $('.StatusResponse').empty().append('<P>The server is running!');
          } else {
              $('.StatusResponse').empty().append('<p>The Server is not started!<br><br><button class=\"btn btn-neutron\" id=\"StartButton\" style=\"margin-top: 5px;\">Start Server</button>');
              $('#StartButton').bind().click(startServer);
          }
       });
   });
});
