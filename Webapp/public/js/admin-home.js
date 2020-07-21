var app = angular.module("admin-home", []); 
var app_url = "http://localhost:3001";

sendAjaxRequest = function(url,callback){
    var xmlhttp = new XMLHttpRequest();
                    xmlhttp.onreadystatechange = function() {
                        if (this.readyState == 4 && this.status == 200) {
                            //console.log(this.responseText);
                            callback(this.responseText);
                        }
                    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

app.controller("admin-homeCtrl", function($scope,$http) {

    var url = app_url + "/getparks";
    $scope.parks = [];

    getParksCallBack = function(json_data){

        data = JSON.parse(JSON.parse(json_data));
        for(var i=0;i<data.length;i++)
        {
            var park = {};
            park.name = data[i].name;
            park.description = data[i].description; 
            park.img_url = data[i].image_url;
            park.park_url = app_url + "/adminpark/" + data[i].id;
            $scope.parks.push(park);
        }
        $scope.$apply();
    }
    sendAjaxRequest(url,getParksCallBack);
    
});

