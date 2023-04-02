# Introduction
This is unofficial https://exchangerate.host (https://github.com/Formicka/exchangerate.host) python client library

# Getting started

## Installation
- Using pip `pip install exchangerate-client`

## Usage
- Get all currency symbols
```
import exchangerate
client = exchangerate.ExchangerateClient()
print(client.symbols())
```

- Get latest rates
```
import exchangerate
client = exchangerate.ExchangerateClient()
print(client.latest())
```

## Configuration
- 

# Development guide
## Testing
This package uses `tox` to run testing automation against multiple python versions, to install and run tox, use

```
pip install tox
tox
```

## Local development
- Install to local env with `pip install --editable .`
- Then this will work `python -c "import exchangerate"`
