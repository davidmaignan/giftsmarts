angular.module('myModule', ['schemaForm'])
       .controller('FormController', function($scope) {
  $scope.schema = {
    "form_name": "Contact Us",
    "form_fields": [
      {
        "field_id": 1,
        "field_title": "Name",
        "field_type": "textfield",
        "field_value": "",
        "field_required": true,
        "field_disabled": false
      },
      {
        "field_id": 2,
        "field_title": "Email",
        "field_type": "email",
        "field_value": "",
        "field_required": true,
        "field_disabled": false
      },
      {
        "field_id": 3,
        "field_title": "Subject",
        "field_type": "dropdown",
        "field_value": "",
        "field_required": true,
        "field_disabled": false,
        "field_options": [
          {
            "option_id": 1,
            "option_title": "General Information",
            "option_value": 1
          },
          {
            "option_id": 2,
            "option_title": "Account Support",
            "option_value": 2
          },
          {
            "option_id": 3,
            "option_title": "Technical Support",
            "option_value": 3
          }
        ]
      },
      {
        "field_id": 4,
        "field_title": "Subject",
        "field_type": "textarea",
        "field_value": "",
        "field_required": true,
        "field_disabled": false
      },
      {
        "field_id": 5,
        "field_title": "I agree to the Terms and Conditions",
        "field_type": "checkbox",
        "field_value": "",
        "field_required": true,
        "field_disabled": false
      }
    ]
  };

  $scope.form = [
    "*",
    {
      type: "submit",
      title: "Save"
    }
  ];

  $scope.model = {};
});
