# Packaging And Publishing the SurRender Python Client

using default python tools or using [uv](https://docs.astral.sh/uv/)

## Prerequisite

Retrieve aforge certificate:

```
curl -X 'GET' 'https://aforge-frdr.biz.nstd.fr.airbusds.corp/portal/api/forge/certificate' -H 'accept: application/x-x509-ca-cert' -o aforge_ca.crt
```

Fill the `~/.pypirc` with:

```
[distutils]
index-servers = local
[local]
repository: https://aforge-frdr.biz.nstd.fr.airbusds.corp/artifactory/api/pypi/aicv-pypi
username: ollagnier <votre compte BIZ ici>
password: <votre token Aforge ici>
```

## File structure

```
├── aforge_ca.crt
├── dist
│   ├── surrender-10.0.0-py3-none-any.whl
│   └── surrender-10.0.0.tar.gz
├── LICENSE
├── pyproject.toml
├── README.md
└── surrender
    ├── geometry.py
    ├── __init__.py
    ├── __pycache__
    ├── surrender_client_base.py
    └── surrender_client.py
```

## Create virtualenv in `src/interfaces/python/surrender`

### Using python3 venv

```
python3 -m venv venv
```

### Using uv

```
uv venv venv
```

## activate venv

```
source venv/bin/activate
```

## Install dependencies

### Using pip

```
pip install ".[build,twine]"
```

### Using uv

```
uv pip install -r pyproject.toml --extra twine
```

## Build Package

### Using pip

```
python -m build
```

### Using uv

```
uv build
```

## Publish

```
python -m twine upload --repository local dist/* --cert aforge_ca.crt
```

## Configure pip to install from private PYPI

`.config/pip/pip.conf`

```
[global]
index-url = https://aforge-frdr.biz.nstd.fr.airbusds.corp/artifactory/api/pypi/gw_files_pythonhosted_org_4dev/simple
# add aicv-pypi registry
extra-index-url = https://aforge-frdr.biz.nstd.fr.airbusds.corp/artifactory/api/pypi/aicv-pypi/simple
trusted-host = aforge-frdr.biz.nstd.fr.airbusds.corp
```
