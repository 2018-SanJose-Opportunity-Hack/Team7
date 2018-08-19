var app = angular.module("issue", []); 
var app_url = "http://localhost:3001";
var complaintId = window.location.pathname.split("/")[2];

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

postComment = function(){
    var description = document.getElementById("description").value;
    var url = app_url +"/postComment?description="+description+"&complaintId="+complaintId;
    sendAjaxRequest(url,postCommentCallback);
}

app.controller("issueCtrl", function($scope,$http) {
    
    var url = app_url + "/getcomplaint?complaintId="+complaintId;
    $scope.parkName = "park name";
    $scope.address = "address";
    $scope.description = "description";
    $scope.numberOfIssues = 0;
    $scope.comments = [];

    getcommentsCallBack = function(json_data){

        data = JSON.parse(JSON.parse(json_data));
        $scope.comments = [];
        $scope.parkName = data.park.name;
        $scope.complaint_img = data.image_url;
        $scope.time = data.time;
        $scope.issue_name = data.title;
        $scope.description = data.description;
        $scope.numberOfComments = data.comments.length;
         for(var i=0;i<$scope.numberOfComments;i++)
        {
            var comment = {};
            comment.user_name = data.comments[i].user.name;
            comment.user_img = data.comments[i].user.image_url;
            comment.timestamp = data.comments[i].time;
            comment.description = data.comments[i].description;
            $scope.comments.push(comment);
        }
        $scope.$apply();
    }
    sendAjaxRequest(url,getcommentsCallBack);

    postCommentCallback = function(){
        sendAjaxRequest(url,getcommentsCallBack);
        document.getElementById("description").value = "";
    }

    
});

