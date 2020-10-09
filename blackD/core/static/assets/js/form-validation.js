function setFormValidation(id) {
  $(id).validate({
    lang: 'pt-BR',
    highlight: function (element) {
      $(element)
        .closest('.form-group')
        .removeClass('has-success')
        .addClass('has-danger');
      $(element)
        .closest('.form-check')
        .removeClass('has-success')
        .addClass('has-danger');
    },
    success: function (element) {
      $(element)
        .closest('.form-group')
        .removeClass('has-danger')
        .addClass('has-success');
      $(element)
        .closest('.form-check')
        .removeClass('has-danger')
        .addClass('has-success');
    },
    errorPlacement: function (error, element) {
      $(element).closest('.form-group').append(error);
    },
  });
}

$(document).ready(function () {
  setFormValidation('#validate-form');
});
