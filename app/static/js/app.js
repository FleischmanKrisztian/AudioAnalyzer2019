// console.log("FLEISCHMAN KRISZTIAN 2/14/2021")

$(document).ready(function(){
    $('form input').change(function () {
      files = this.files;
      $('form p').text(files[0].name + " selected");
    });
  });