# Researcher Facing Read the Docs

## Developer Notes

### Images

- Use `**/images` to store images in each subfolder.
- Use `.. figure:: ./images/<image_file>` to reference images.
- All `figure::` must have a descriptive `:alt:` text.
- Use maximally-compressed `*.png` file format for images.

### Links

- External targets should be anonymous, not explicit. Single underscores are "explicit targets", double underscores are "anonymous targets". External links should be formatted as ``Link text `<URL>`__``, note the double underscore.

### Known Issues

- Some inline languages add an `<s>` tag in html, leading to strikethroughs. This occurs for string literals in MATLAB and R.