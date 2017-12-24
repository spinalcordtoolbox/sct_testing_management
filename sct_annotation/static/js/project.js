/* Project specific Javascript goes here. */

/*
Formatting hack to get around crispy-forms unfortunate hardcoding
in helpers.FormHelper:

    if template_pack == 'bootstrap4':
        grid_colum_matcher = re.compile('\w*col-(xs|sm|md|lg|xl)-\d+\w*')
        using_grid_layout = (grid_colum_matcher.match(self.label_class) or
                             grid_colum_matcher.match(self.field_class))
        if using_grid_layout:
            items['using_grid_layout'] = True

Issues with the above approach:

1. Fragile: Assumes Bootstrap 4's API doesn't change (it does)
2. Unforgiving: Doesn't allow for any variation in template design
3. Really Unforgiving: No way to override this behavior
4. Undocumented: No mention in the documentation, or it's too hard for me to find
*/
$('.form-group').removeClass('row');
$('a.btn-dataset').click( function (event) {
  var href = $(this).attr('dataset_href');
  $(this).after('<div></div>');
  $(this).next().load(href);
  event.preventDefault();
});

// Dynamically load the dataset form
$(".collapse").on('show.bs.collapse', function(){
  var body = $(this).find('.card-body')[0];
  var href = $(this)[0].attributes['href-form'].value;
  var xhr = new XMLHttpRequest();

  xhr.onload = function() {
    body.innerHTML = this.response;
  };
  xhr.open('GET', href, true);
  xhr.send();
});
