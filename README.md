# RKC Cli

## Setup

1. Install [direnv](https://direnv.net/docs/installation.html)
2. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
3. Run `uv venv` to create virtual env
4. Run `cp .envrc.example .envrc`
5. Run `direnv allow`
6. Run `uv sync`

## Documentation

```shell
mkdocs build
mkdocs serve
```

# Usage

Login & capture

```shell
rkc-cli login && rkc-cli read-forum -S "»" https://campus.college.ch/forum/posts/105396-unit-2-theorising-leadership 1
```