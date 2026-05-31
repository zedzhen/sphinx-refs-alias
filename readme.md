Add support alias for reference.

## Configs
`reference_aliases: dict[str, str | tuple[str, str | None]]`

The key is an alias.

If the value is a string, then it is equivalent to a tuple `(value, None)`.

If the value is a tuple:
* `value[0]` is the real name
* `value[1]` (if is not None) displayed text
