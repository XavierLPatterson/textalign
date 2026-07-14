"""Useful tools for creating, aligning and wrapping `str`s."""
#
## Created by XLP
##     github@XavierLPatterson
##     khanacademy@UnavailablePIZZAtype
## Released under the MIT license
#
from collections.abc import Callable, Iterable
from itertools       import cycle, islice, zip_longest
from typing          import (
    Concatenate,
    Literal,
    Optional,
    ParamSpec,
    TypeVar,
    final
)

## Types
_T = TypeVar('_T'); P = ParamSpec('P')
type AlignType                 = Literal[0, 1, 2, 3]
type StrsProtocol              = Callable[Concatenate[str, P], _T]
type WrapFunc                  = Callable[[int, int, int, str], Iterable | None]
## Constants
LEFT:        AlignType         = 0
CENTER:      AlignType         = 1
RIGHT:       AlignType         = 2
SPACED:      AlignType         = 3
BACKSPACE:   Literal['\b']     = '\b'
DELETE:      Literal['\u007f'] = '\u007f'
NULLSTR:     Literal['\0']     = '\0'
## Defaults
STRING:      str               = ''
WIDTH:       int               = 30
ALIGNMENT:   int               = LEFT
FILL:        str               = ' '
BORDER:      str               = '|'
FROMSIDE:    int               = 2
# Priority side when it comes to math
PRIORITY:    int               = LEFT
TABSIZE:     int               = 4
PLACEHOLDER: str               = '...'
FORCECLIP:   bool              = False
MAXLINES:    int               = -1 # -n = disabled
# The char used to determine spacing points
SPACECHAR:   str               = ' '

## Decorator
def strs(f: StrsProtocol) -> StrsProtocol:
    """Decorator that keeps newlines (`\\r`, `\\n`,
    and `\\r\\n`) at the end of the `string` while
    also expanding tabs (`\\t`) into spaces.
    
    **Disable by setting `strs` keyword argument
    to a falsy value within an `@strs` decorated
    function**"""
    def _(
            string:   str,
            *args:    P.args,
            **kwargs: P.kwargs
        ) -> str | _T:
        if not kwargs.get('strs', True):
            kwargs.pop('strs')
            return f(string, *args, **kwargs)
        if not ('\n' in (
                s := string.expandtabs(TABSIZE)
            ) or '\r' in s):
            return f(s, *args, **kwargs)
        ls = s.splitlines(True)
        return ''.join([
            f(l[:(
                i := -2 if '\r\n' in l else -1
            )], *args, **kwargs) + l[i:]
                for l in ls[:-1]
        ]) + f(ls[-1], *args, **kwargs)
    return _

## Internal function
def __WRAP__(i: int, _i: int, w: int, string: str) -> str | None:
    """Default internal function used for wrapping.
    
    **Not a standalone function!**"""
    if string[i - 1].isspace():
        return '\b\n'
    # elif string[i].isspace():
    #     return '\n\u007f'
    elif string[i - 1] == '-' and not string[i].isnumeric():
        return '\n'
    return None

## Functions
@strs
def align(
        string:    str          =STRING,
        /,
        width:     int          =WIDTH,
        alignment: AlignType    =ALIGNMENT,
        fill:      str          =FILL,
        fromside:  int          =FROMSIDE,
        priority:  AlignType    =PRIORITY,
        *,
        lfill:     Optional[str]=None,
        rfill:     Optional[str]=None
    ) -> str:
    """Return a **copy** of `string` aligned
    left, center, right, or spaced.
    
    NOTE:
        Spaced alignment will consume
        whatever is consider a SPACECHAR
        and replace it with chars from
        `fill` value."""
    w  = width - len(string)
    lf = lfill or fill
    rf = rfill or fill
    if alignment == LEFT:
        return rstr(
            lf, min(w, fromside)
        ) + string + rstr(
            rf, w - fromside
        )
    if alignment == CENTER:
        p = [(w / 2).__ceil__(), w // 2]
        if priority == RIGHT:
            p.reverse()
        return rstr(
            lf, p[0]
        ) + string + rstr(
            rf, p[1]
        )
    if alignment == RIGHT:
        return rstr(
            lf, w - fromside 
        ) + string + rstr(
            rf, min(w, fromside)
        )
    if alignment == SPACED:
        try:
            # string will be squished if width is too small
            ws   = string.split(SPACECHAR)
            l    = len(ws) - 1
            b, x = divmod(width - len(''.join(ws)), l)
            s    = [
                rstr(fill, b + (
                    1 if x - i > 0 else 0
                )) for i in range(l)
            ]
            if priority == RIGHT: # too lazy to do maths instead
                s.reverse()
            return ''.join([
                i0 + i1 for i0, i1 in zip_longest(
                    ws, s, fillvalue=''
                )
            ])
        except ZeroDivisionError:
            return string
    raise ValueError(f'alignment type not recognized!')

@strs
def alignwrap(
        string:    str,
        /,
        width:     int               =WIDTH,
        wrapwidth: int               =WIDTH // 2,
        alignment: AlignType         =ALIGNMENT,
        fill:      str               =FILL,
        fromside:  int               =FROMSIDE,
        priority:  AlignType         =PRIORITY,
        wrapkey:   Optional[WrapFunc]=None,
        maxlines:  int               =MAXLINES,
        *,
        lfill:     Optional[str]     =None,
        rfill:     Optional[str]     =None
    ) -> str:
    """Align wrapped lines from a **copy** of `string`.
    
    NOTE:
        Rules/NOTEs from `align` and `wrap`
        still apply

    **Sorthand that bypasses multiple newline checks
    when calling `align(wrap(...), ...)`**"""
    return '\n'.join([
        align(
            line, width, alignment, fill, fromside, priority,
            lfill=lfill, rfill=rfill, strs=False
        ) for line in wrap(
            string, wrapwidth, wrapkey, maxlines,
            strs=False
        ).splitlines()
    ])

@strs
def clip(
        string: str,
        /,
        width:  int,
        ending: str =PLACEHOLDER,
        force:  bool=FORCECLIP
    ) -> str:
    """Clip a **copy** of `string` within `width` having
    `ending` as the final char(s).
    
    NOTE:
        If `force` then `ending` will be added
        no matter proper _positioning_."""
    w = min(width, ( l := len(ending) ))
    n = max(width - l, 0)
    if force:
        return string[:n] + ending[:w]
    return (s := string[:n])[:n if (
        i := s.rfind(SPACECHAR)
    ) == -1 else i] + ending[:w]

def delback(string: str) -> str:
    """Remove backspace/delete ASCII decimals along
    with the previous/next value from a **copy** of
    `string`."""
    ba = bytearray(string, 'utf-8')
    while True:
        if (i := ba.find(8)) != -1:
            ba.pop(i)
            if i != 0:
                ba.pop(i - 1)
        elif (i := ba.rfind(127)) != -1:
            if i != len(ba) - 1:
                ba.pop(i)
            ba.pop(i)
        else:
            return ba.decode()

def rstr(
        string: str,
        width:  int
    ) -> str:
    """Repeat a **copy** of `string` until the
    returned `str` is `width` in size."""
    return '' if width < 0 else ''.join(
        islice(cycle(string), width)
    )

@strs
def wrap(
        string:    str,
        /,
        width:     int               =WIDTH,
        key:       Optional[WrapFunc]=None,
        maxlines:  int               =MAXLINES,
        ending:    str               =PLACEHOLDER,
        forceclip: bool              =False
    ) -> str:
    """Wrap a **copy** of `string` within the given `width`,
    optionally using a `key` function for the wrapping,
    stopping upon a **total** of `maxlines` lines where the
    last line ends with `ending`.
    
    NOTE:
        A `width < 2` won't actually wrap things.
        Wrapping will imediately stop upon finding
        a null (\\0) char within the `str` returned
        by `key`.
        Negative values disables `maxlines`.
        Any extra text outside the maximum amount of
        lines is truncated using `clip`.
        `key` may return `str`s containing
        backspace/delete ASCII chars to
        manipulate output."""
    k = key or __WRAP__; s = ''; L = len(string)
    j = l = 0; t0 = t1 = (-1, None)
    for i in range(1, L):
        b = ( t0 := (i, k(
            i, max(j, t1[0]), width, string
        )) )[1] is not None
        if i - j == width:
            s0 = s1 = ''
            if (t := t0 if b else t1)[0] - j < 1:
                if string[i].isalpha() and string[i - 1].isalpha():
                    s0 = string[j:i - 1]; s1 = '-\n'; j -= 1
                else:
                    s0 = string[j:i]; s1 = '\n'
                j += width
            else:
                s0 = string[j:t[0]]; j += t[0] - j
                for c in t[1]:
                    if c == NULLSTR:
                        return delback(s + s0 + s1)
                    s1 += c
            if 0 < maxlines <= (l := l + 1):
                return delback(s + clip(s0, width, ending, forceclip))
            s += s0 + s1
        elif b:
            t1 = tuple(t0)
    return delback(s + string[j:])

## Other
class _version(tuple):
    @final
    @property
    def major(self) -> int:
        """Major version."""
        return 5
    @final
    @property
    def minor(self) -> int:
        """Minor version."""
        return 0
    def __repr__(self):
        return f'v{self.major}.{self.minor}'
version:     _version          = _version([5, 0])
__version__: str               = version.__repr__()
__all__:     list[str]         = [n for n in globals() if n[0] != '_']
### last update: July 14, 2026
