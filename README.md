[![Build Status](https://travis-ci.org/dustinbrown/anydo_cli.svg?branch=master)](https://travis-ci.org/dustinbrown/anydo_cli)
[![Coverage Status](https://coveralls.io/repos/github/dustinbrown/anydo_cli/badge.svg?branch=master)](https://coveralls.io/github/dustinbrown/anydo_cli?branch=master)

# anydo_cli - anydo actions from the command line
## Requirements
python 3.5+
## Usage
### create tasks
`$ anydo create 'drink water'`

### list due tasks 
`$ anydo due_tasks`

### snooze due task
`$ anydo snooze 'drink water'`

## Troubleshooting
### Running tests
Since click and python3 don't play nice, set the following to your local. This is an example for US. More information can be found at http://click.pocoo.org/5/python3/#python3-surrogates

```
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```

