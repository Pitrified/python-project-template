# Params vs config

## Overview

add in sample params the correct config/params splitting with env type
analyze the various pattern we are exposing in the codebase, matching them with ok/no comments

objective: enhance
src/project_name/config/sample_config.py
src/project_name/params/sample_params.py
then write extensive docstrings in that module to keep it well documented
plus dedicated docs in `docs/` to explain the pattern and how to use it
and reference that in the copilot instructions as well

status and sample usage:

src/project_name/config/sample_config.py
ok: clean, concise.
add: an attribute which is SecretStr

src/project_name/params/sample_params.py
no: too simple, must be enhanced to show the pattern of env location/type switching

src/project_name/params/webapp/webapp_params.py
ok: uses the correct pattern of env location/type switching
no: loads the non-secret config values from env. if something is not secret, we can write it directly in the params file, setting the attribute. if it changes in between environments, we have the machinery of stage/location exactly for this

src/tg_central_hub_bot/params/bot_params.py
src/tg_central_hub_bot/config/bot_config.py
ok:
receives EnvType as single argument, even if not used -> future proof
use of SecretStr for the token
no:
should move the getenv-check-convert_to_secret pattern to some utility function. do not raise a custom exception, just notify which variable is missing and let it raise the standard error
the token loading should be in a `load_common_params` to keep `init` small with just the call

src/project_name/params/project_name_paths.py
ok: shows the match case on env type to load different values

## Plan

### Positive patterns to consolidate

Collected from the analysis above:

| Pattern | Source |
|---|---|
| `BaseModelKwargs` for config models | `sample_config.py`, `bot_config.py` |
| `SecretStr` field in config; masked in `__str__` of Params | `bot_config.py`, `bot_params.py` |
| `env_type: EnvType` as sole constructor arg (future-proof even if unused) | `bot_params.py`, `project_name_paths.py` |
| `__init__` only calls `_load_params()` | `project_name_paths.py` |
| `_load_params()` calls `_load_common_params()` then dispatches via `match` on stage and location | `project_name_paths.py` |
| `_load_common_params()` sets common defaults; env-specific methods define other attributes, that are env dependent. no redefinition, one source of truth (per env). | `project_name_paths.py` |
| Secret env vars loaded with `os.environ["VAR"]` (raises `KeyError` naturally, no custom exception) | critique of `bot_params.py` |
| Secret loading extracted into a tiny module-level helper `_load_secret(var_name)` | critique of `bot_params.py` |
| Non-secret values are literals in params code, not `os.getenv()` reads | critique of `webapp_params.py` |
| `to_config()` assembles and returns the Pydantic config model | all params classes |

---

### Changes to `sample_config.py`

1. Add `secret_api_key: SecretStr` field to `SampleConfig`.
   - No other changes; the file is already clean and concise.

Resulting shape:

```python
class SampleConfig(BaseModelKwargs):
    some_int: int
    nested_model: NestedModel
    secret_api_key: SecretStr
    kwargs: dict = Field(default_factory=dict)
```

---

### Changes to `sample_params.py`

Full rewrite to demonstrate all consolidated patterns:

**1. Module-level secret-loading helper**

```python
def _load_secret(var_name: str) -> SecretStr:
    """Load a secret from an environment variable.

    Raises KeyError with the variable name if not set.
    """
    return SecretStr(os.environ[var_name])
```

**2. Constructor - single `env_type` arg, delegates to `_load_params()`**

```python
def __init__(self, env_type: EnvType) -> None:
    self.env_type = env_type
    self._load_params()
```

**3. `_load_params()` - orchestrates common load + stage + location dispatch**

keep it as focused as possible in the real params classes, but for this sample we want the full cartesian product of stage/location to show the pattern clearly

```python
def _load_params(self) -> None:
    self._load_common_params()
    match self.env_type.stage:
        case EnvStageType.DEV:
            self._load_dev_params()
        case EnvStageType.PROD:
            self._load_prod_params()
        case _:
            raise UnknownEnvStageError(self.env_type.stage)

def _load_dev_params(self) -> None:
    self.some_int = 7  # example of a value that changes with stage, not with location
    match self.env_type.location:
        case EnvLocationType.LOCAL:
            self._load_dev_local_params()
        case EnvLocationType.RENDER:
            self._load_dev_render_params()
        case _:
            raise UnknownEnvLocationError(self.env_type.location)

... # similar for prod
```

**4. `_load_common_params()` - literal defaults; loads secret from env**

```python
def _load_common_params(self) -> None:
    # Non-secret values: set as literals, not os.getenv()
    self.nested_model_some_str: str = "Hello, Params!"
    self.custom_kwargs: dict = {"key1": "value1", "key2": "value2"}
    # Secret value: loaded from env; KeyError raised naturally if missing
    self.secret_api_key: SecretStr = _load_secret("SAMPLE_API_KEY")
```

**5. Stage-specific: set only what differs**

```python
def _load_dev_params(self) -> None:
    self.some_int = 7  

def _load_prod_params(self) -> None:
    self.some_int = 42
```

**6. Location-specific: same principle**

as above.

**7. `to_config()` - assembles the Pydantic config model**

```python
def to_config(self) -> SampleConfig:
    return SampleConfig(
        some_int=self.some_int,
        nested_model=NestedModel(some_str=self.nested_model_some_str),
        secret_api_key=self.secret_api_key,
        kwargs=self.custom_kwargs,
    )
```

**8. `__str__` - mask the secret**

```python
def __str__(self) -> str:
    s = "SampleParams:"
    s += f"\n  env_type: {self.env_type}"
    s += f"\n  some_int: {self.some_int}"
    s += f"\n  nested_model_some_str: {self.nested_model_some_str}"
    s += f"\n  secret_api_key: [REDACTED]"
    s += f"\n  custom_kwargs: {self.custom_kwargs}"
    return s
```

---

### Downstream tasks (out of scope for this plan, tracked separately)

- Rewrite docstrings in both files to fully document every decision (why `env_type` even if unused, why literals not `os.getenv`, why `KeyError` not custom exception).
- Add `docs/guides/params-config.md` explaining the pattern end-to-end.
- Reference the new doc page in `copilot-instructions.md` Key patterns section.
