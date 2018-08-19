var app = angular.module("park", []); 
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

app.controller("parkCtrl", function($scope,$http) {
    var parkId = window.location.pathname.split("/")[2];
    var url = app_url + "/getpark?parkId="+parkId;
    $scope.parkName = "park name";
    $scope.address = "address";
    $scope.description = "description";
    $scope.numberOfIssues = 0;
    $scope.complaints = [];

    getParkCallBack = function(json_data){

        data = JSON.parse(JSON.parse(json_data));
        
        $scope.parkName = data.name;
        $scope.address = data.address;
        $scope.description = data.description;
        $scope.numberOfIssues = data.complaints.length;
        for(var i=0;i<$scope.numberOfIssues;i++)
        {
            var complaint = {};
            complaint.user_name = data.complaints[i].user.name;
            complaint.user_img = data.complaints[i].user.image_url;
            complaint.timestamp = data.complaints[i].time;
            complaint.title = data.complaints[i].title;
            complaint.description = data.complaints[i].description;
            complaint.status = data.complaints[i].status.name;
            complaint.issue_url = "../issue/"+data.complaints[i].id.S;
            //complaint.status = "IN_PROGRESS";
            $scope.complaints.push(complaint);
        }
        $scope.$apply();
    }
    sendAjaxRequest(url,getParkCallBack);
    
});

