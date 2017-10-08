var phonecatApp = angular.module('app', []);

// Define the `PhoneListController` controller on the `phonecatApp` module
phonecatApp.controller('ctrl', function ($scope, $timeout) {
    $scope.list = {};

    $scope.selected = [];
    $scope.sumTime = 0;
    $scope.selectedModels = {};
    $scope.selectedChange = function (name) {
        if ($scope.selectedModels[name]) {
            $scope.selected.push(name)
        } else {
            delete $scope.selected.splice($scope.selected.indexOf(name), 1);
        }
    };

    $scope.clear = function(){
        BackEnd.clear_timer();
    }

    // window.setTimeout(function () {
    window.setInterval(function () {
        var nfo = BackEnd.get_info();

        var l = [];
        var allTime = 0;

        var sumTime = 0;

        angular.forEach(JSON.parse(nfo), function (time, appName) {
            l.push({name: appName, time: time});
            allTime += time;
            if ($scope.selected.indexOf(appName) > -1) {
                sumTime += time;
            }
        });

        $scope.list = l.sort(function (a, b) {
            if (a.time < b.time)
                return 1;
            if (a.time > b.time)
                return -1;
            return 0;
        });

        $scope.allTime = allTime;
        $scope.sumTime = sumTime;

        $scope.$apply()
    }, 1000);
});