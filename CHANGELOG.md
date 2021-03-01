# Changelog

## v2.0.0

### Changes:

- Add liveserver support for `react-scripts@4.0.0` and up
- Added new `CRA_PACKAGE_JSON_HOMEPAGE` setting for Django **settings.py** to help contact liveserver when the Create-React-App project's **package.json** contains a value for `"homepage"`.

### Breaking Changes:
- Remove `json` template tag for Django's built-in `json_script`.

To update your code, change the following in your HTML file that loads your React:

```html
{% load cra_helper_tags %}
<html>
  <!-- ..snip.. -->
  <body>
    <!-- ..snip.. -->
    <script>
      window.component = '{{ component }}';
      window.props = {{ props | json }};
      window.reactRoot = document.getElementById('react');
    </script>
  </body>
</html>
```

To use Django's `json_script` template tag instead:

```html
<html>
  <!-- ..snip.. -->
  <body>
    <!-- ..snip.. -->
    {{ props | json_script:"react-props" }}

    <script>
      window.component = '{{ component }}';
      window.props = JSON.parse(
        document.getElementById('react-props').textContent
      );
      window.reactRoot = document.getElementById('react');
    </script>
  </body>
</html>
```
