app = angular.module("app", (app_modules || []));

function TopLevelController($scope, $http) {
    $scope.data = [];
    $http.get('data.json').success(function(data) {
        $scope.data = data;
    });
}
