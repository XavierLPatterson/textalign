> [!NOTE]
> I personally believe a **better** explanation and **easier** copy-paste-code is on Khan Academy [here](https://www.khanacademy.org/python-program/textalignpy-51-module/6454969571328000).

# textalign

Useful tools for creating, wrapping, clipping, repeating and aligning Python strings (`str`).

## Features
- _Constants_ for ease of use (LEFT, CENTER, RIGHT, SPACED, etc.)
- Customizability for... customizability
- align: left, center, right, and spaced alignment with custom fill, positioning and odd number side prioritizing
```python
def align(
    string: Optional[str] = ...,
    /,
    width: Optional[int] = ...,
    alignment: Optional[AlignType] = ...,
    fill: Optional[str] = ...,
    fromside: Optional[int] = ...,
    priority: Optional[AlignType] = ...,
    *,
    lfill: Optional[str] = ...,
    rfill: Optional[str] = ...
) -> str: ...
```
- wrap: line-wrapping with customizable wrap-key behavior and support for max lines & clipping
```python
def wrap(
    string: Optional[str] = ...,
    /,
    width: Optional[int] = ...,
    key: Optional[WrapFunc] = ...,
    maxlines: Optional[int] = ...,
    ending: Optional[str] = ...,
    forceclip: Optional[bool] = ...
) -> str: ...
```
- alignwrap: align wrapped lines efficiently
```python
def alignwrap(
    string: Optional[str] = ...,
    /,
    width: Optional[int] = ...,
    wrapwidth: Optional[int] = ...,
    alignment: Optional[AlignType] = ...,
    fill: Optional[str] = ...,
    fromside: Optional[int] = ...,
    priority: Optional[AlignType] = ...,
    wrapkey: Optional[WrapFunc] = ...,
    maxlines: Optional[int] = ...,
    ending: Optional[str] = ...,
    forceclip: Optional[bool] = ...,
    *,
    lfill: Optional[str] = ...,
    rfill: Optional[str] = ...
) -> str: ...
```
- clip: length-based clipping with optional forced endings/placeholder
```python
def clip(
    string: Optional[str] = ...,
    /,
    width: Optional[int] = ...,
    ending: Optional[str] = ...,
    force: Optional[bool] = ...,
    always: Optional[bool] = ...
) -> str: ...
```
- textalign3: original alignment style from textalign v3 that allows batching multi-line alignment with border support and iterable parameters
```python
def textalign3(
    string: Optional[str | Iterable[str]] = ...,
    /,
    width: Optional[int | Iterable[int]] = ...,
    fill: Optional[str | Iterable[str]] = ...,
    border: Optional[str | Iterable[str]] = ...,
    fromSide: Optional[int | Iterable[int]] = ...,
    *,
    lfill: Optional[str | Iterable[str]] = ...,
    rfill: Optional[str | Iterable[str]] = ...,
    lborder: Optional[str | Iterable[str]] = ...,
    rborder: Optional[str | Iterable[str]] = ...,
    priority: Optional[int | Iterable[int]] = ...,
    alignment: Optional[int | Iterable[int]] = ...
) -> str: ...
```
- delback: handles ASCII backspace/delete when building strings programmatically
```python
def delback(string: str) -> str: ...
```
- rstr: repeat a string until it is `width` in length
```python
def rstr(string: str, width: int) -> str: ...
```
- ifNotNone: if a is none then b
```python
def ifNotNone(a: Any, b: Any) -> type(a) | type(b): ...
```
- `@strs`: decorator to preserve trailing newline(s) and expand tabs
```python
def strs(f: Callable[[str, ...], ...]) -> Callable[[str, ...], ...]: ...
```

## Installation

Install directly from the repository (development / latest):

pip:
```bash
pip install git+https://github.com/XavierLPatterson/textalign.git
```

Or clone and import locally:
```bash
git clone https://github.com/XavierLPatterson/textalign.git
cd textalign
# use main.py as a module or package in your project
```

## Quick usage

Basic imports:
```python
from textalign import (
    align, alignwrap, wrap, clip, textalign3, delback,
    LEFT, CENTER, RIGHT, SPACED, PLACEHOLDER, version
)
```

align — align single line (default fill = ' ', default width = 30)
```python
# default LEFT alignment with default fromside (2)
s = align("hello", width=10)
# result: two spaces, "hello", then three spaces -> "  hello   "
```

CENTER or RIGHT alignment:
```python
s = align("hello", width=11, alignment=CENTER)
# center-aligned inside 11 characters

s = align("hello", width=10, alignment=RIGHT)
# right-aligned inside width 10
```

SPACED alignment — distribute fill characters across spaces:
```python
s = align("a b c", width=11, alignment=SPACED, fill='.')
# spaces between words are replaced by repeated '.' to fill width
```

wrap — break a long string into lines with a wrap-key (defaults to intelligent breakpoints)
```python
text = "This is a longer sentence that will be wrapped."
wrapped = wrap(text, width=12)
print(wrapped)
# wrapped -> multiple lines no longer than 12 characters (default key handles spaces and hyphens)
```

alignwrap — wrap then align each wrapped line:
```python
aligned_wrapped = alignwrap(text, width=20, wrapwidth=12, alignment=CENTER)
print(aligned_wrapped)
```

clip — force a string to fit in a width and optionally add an ending (placeholder)
```python
short = clip("This is long", width=8)                # default PLACEHOLDER '...'
short_force = clip("This is long", width=8, force=True)
short_always = clip("short", width=8, always=True)   # will add ending even if it fits
```

textalign3 — batch/multi-line alignment that supports iterable parameters and borders
```python
print(textalign3(
    ["one", "two longer line", "three"],
    width=[20, 20, 20], fill=' ', border='|',
    alignment=[LEFT, CENTER, RIGHT]
))
# Produces multiple lines, each aligned per the iterable arguments with borders applied
```

delback — handles backspace (ASCII 8) and delete (ASCII 127) by removing adjacent chars:
```python
s = "ab" + "\b"  # backspace removes previous char
print(delback(s))  # prints "a" behavior handled safely
```

Utilities:
```python
# rstr repeats a string to a given width
from textalign import rstr
print(rstr('*', 5))  # ***** 

# version
from textalign import __version__
print(__version__)  # v5.1
```

## License

Released under the MIT license.
