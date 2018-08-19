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

postcomplaint = function()
{
    var park_elem = document.getElementById("parks");
    var park = park_elem.options[park_elem.selectedIndex].value;
    var category_elem = document.getElementById("category");
    var category = category_elem.options[category_elem.selectedIndex].value;
    var image_url = "url to S3 bucket";
    var description = document.getElementById("description").value;
    var title = document.getElementById("title").value;
    var callback = document.getElementById("callback").checked ? "Yes" : "No";
    var url = app_url + "/postcomplaint?park="+park+"&category="+category+"&image_url="+image_url+"&description="+description+"&title="+title+"&callback="+callback;
    sendAjaxRequest(url,postcomplaintCallBack);
}

postcomplaintCallBack = function(data){
        alert("sucessfully registed a complaint");
}

var app = angular.module("complaint", []); 

app.controller("complaintCtrl", function($scope,$http) {

    $scope.categories = [{"name":"one","id":"adsnf"}];
    $scope.parks = [{"name":"one","id":"adsnf"}];
    
    getParksCallBack = function(json_data){
        $scope.parks = [];
        //$scope.$apply();
        data = JSON.parse(JSON.parse(json_data));
        for(var i=0;i<data.length;i++)
        {
            var park = {};
            park.name = data[i].name;
            park.id = data[i].id;
            $scope.parks.push(park);
        }
       sendAjaxRequest(app_url+"/getcategories",getCategoriesCallBack);
    }
    getCategoriesCallBack = function(json_data){
        $scope.categories = [];
        data = JSON.parse(JSON.parse(json_data));
        for(var i=0;i<data.length;i++)
        {
            var category = {};
            category.name = data[i].name;
            category.id = data[i].id;
            $scope.categories.push(category);
        }
        // document.getElementsByClassName("custom-select-menu")[0].style.display = "none";
        // document.getElementsByClassName("custom-select-menu")[1].style.display = "none";

        $scope.$apply();
    }
    sendAjaxRequest(app_url+"/getparks",getParksCallBack);

    
    
});

