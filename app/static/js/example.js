angular.module('ui.bootstrap').controller('TypeaheadCtrl', function($scope, $http, $window) {

  var _selected;


  $scope.getLocation = function(val) {
    return $http.get('/rest/zaprimkas', {
      params: {
        upit: val,
      }
    }).then(function(response){
      return response.data.results.map(function(item){
        return item.id+', '+item.ime_koperanta+', '+item.prezime_koperanta;
      });
    });
  };

  $scope.onSelect = function($item, $model, $label) {
    $scope.$item = $item;
    $scope.$model = $model;
    $scope.$label = $label;
    $window.location.href = '/home/edit_zaprimka/'+$item.split(",")[0];
    };



});