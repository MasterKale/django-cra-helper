# Steps for Publishing

Because it's always so long between releases...

## Requirements

- Twine

Twine can be installed system-wide without using `sudo`:

```sh
$> pip install --user --upgrade twine
```

## Step-by-step

### 1. Remove previous build output:

```sh
$> rm -rf build/ dist/ django_cra_helper.egg-info/
```

### 2. Build the library:

```sh
$> python3 setup.py sdist bdist_wheel
```

### 3. Check files with twine:

```sh
$> python3 -m twine check dist/*
```

You should see output like this:

> Checking dist/django_cra_helper-1.2.2-py3-none-any.whl: PASSED
> Checking dist/django-cra-helper-1.2.2.tar.gz: PASSED

### 4. Upload to TestPyPi:

```sh
$> python3 -m twine upload -r testpypi dist/*
```

### 5. Verify everything looks fine on TestPyPI:

https://test.pypi.org/project/django-cra-helper/

### 6. After confirming, publish to real PyPI:

```sh
$> python3 -m twine upload dist/*
```

### 7. Check it out on PyPI:

https://pypi.org/project/django-cra-helper/
