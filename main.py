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
type AT_iAT                    = AlignType | Iterable[AlignType]
type int_iint                  = int | Iterable[int]
type str_istr                  = str | Iterable[str]
type StrsProtocol              = Callable[Concatenate[str, P], _T]
type WrapFunc                  = Callable[
    [int, int, int, str], Iterable | None
]
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
# Always place the placeholder when using clip
ALWAYSPLACE: bool              = False
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
            string:   Optional[str]=None,
            *args:    P.args,
            **kwargs: P.kwargs
        ) -> str | _T:
        if not kwargs.get('strs', True):
            kwargs.pop('strs')
        elif (string is not None) and ('\n' in (
                s := string.expandtabs(TABSIZE)
            ) or '\r' in s):
            ls = s.splitlines(True)
            return ''.join([
                f(l[:(
                    i := -2 if '\r\n' in l else -1
                )], *args, **kwargs) + l[i:]
                    for l in ls[:-1]
            ]) + f(ls[-1], *args, **kwargs)
        return f(string, *args, **kwargs)
    return _

## Internal functions
def __GINTS__(
        obj: int | Iterable[int]
    ) -> list[int]:
    """Get ints from `obj`.
    
    `return [obj] if obj int else [ints in obj]`"""
    return [i for i in (
        [obj] if isinstance(obj, int)
            else obj
    )]
def __GSTRS__(
        obj: str | Iterable[str]
    ) -> list[str]:
    """Get strs from `obj`.
    
    `return [obj] if obj str else [strs in obj]`"""
    if isinstance(obj, Iterable) \
       and not isinstance(obj, str):
        obj = '\n'.join([ifNotNone(s, '') for s in obj])
    return obj.expandtabs(TABSIZE).splitlines()
def __WRAP__(i: int, _i: int, w: int, string: str) -> str | None:
    """Default internal function used for wrapping.
    
    **Not a standalone function!**"""
    if string[i - 1].isspace():
        return '\b\n'
    # elif string[i].isspace():
    #     return '\n\u007f'
    elif string[i - 1] == '-' and not string[i].isnumeric():
        return '\n'

## Functions
@strs
def align(
        string:    Optional[str]      =None,
        /,
        width:     Optional[int]      =None,
        alignment: Optional[AlignType]=None,
        fill:      Optional[str]      =None,
        fromside:  Optional[int]      =None,
        priority:  Optional[AlignType]=None,
        *,
        lfill:     Optional[str]      =None,
        rfill:     Optional[str]      =None
    ) -> str:
    """Return a **copy** of `string` aligned
    left, center, right, or spaced.
    
    NOTE:
        Spaced alignment will consume
        whatever is consider a SPACECHAR
        and replace it with chars from
        `fill` value."""
    f  = ifNotNone(fill, FILL)
    lf = lfill or f; rf = rfill or f
    w  = (width or WIDTH) - len(s := ifNotNone(string, STRING))
    if (a := ifNotNone(alignment, ALIGNMENT)) == LEFT:
        return rstr(
            lf, min(w, (fs := ifNotNone(fromside, FROMSIDE)))
        ) + s + rstr(
            rf, w - fs
        )
    if a == CENTER:
        p = [(w / 2).__ceil__(), w // 2]
        if ifNotNone(priority, PRIORITY) == RIGHT:
            p.reverse()
        return rstr(
            lf, p[0]
        ) + s + rstr(
            rf, p[1]
        )
    if a == RIGHT:
        return rstr(
            lf, w - (fs := ifNotNone(fromside, FROMSIDE)) 
        ) + s + rstr(
            rf, min(w, fs)
        )
    if a == SPACED:
        try:
            # string will be squished if width is too small
            ws   = s.split(SPACECHAR)
            l    = len(ws) - 1
            b, x = divmod((width or WIDTH) - len(''.join(ws)), l)
            ss   = [
                rstr(f, b + (
                    1 if x - i > 0 else 0
                )) for i in range(l)
            ]
            # too lazy to do maths instead xP
            if ifNotNone(priority, PRIORITY) == RIGHT:
                ss.reverse()
            return ''.join([
                i0 + i1 for i0, i1 in zip_longest(
                    ws, ss, fillvalue=''
                )
            ])
        except ZeroDivisionError:
            # didn't really know what to do heheh...
            return s or rstr(f, w)
    raise ValueError(f'alignment type not recognized!')

@strs
def alignwrap(
        string:    Optional[str]      =None,
        /,
        width:     Optional[int]      =None,
        wrapwidth: Optional[int]      =None,
        alignment: Optional[AlignType]=None,
        fill:      Optional[str]      =None,
        fromside:  Optional[int]      =None,
        priority:  Optional[AlignType]=None,
        wrapkey:   Optional[WrapFunc] =None,
        maxlines:  Optional[int]      =None,
        ending:    Optional[str]      =None,
        forceclip: Optional[bool]     =None,
        *,
        lfill:     Optional[str]      =None,
        rfill:     Optional[str]      =None
    ) -> str:
    """Align wrapped lines from a **copy** of `string`.
    
    NOTE:
        Rules/NOTEs from `align` and `wrap`
        still apply.

    **Sorthand that bypasses multiple newline checks
    when calling `align(wrap(...), ...)`**"""
    return '\n'.join([
        align(
            line, width, alignment, fill, fromside, priority,
            lfill=lfill, rfill=rfill, strs=False
        ) for line in wrap(
            string, wrapwidth or WIDTH // 2, wrapkey, maxlines, ending,
            forceclip, strs=False
        ).splitlines() or ['']
    ])

@strs
def clip(
        string: Optional[str] =None,
        /,
        width:  Optional[int] =None,
        ending: Optional[str] =None,
        force:  Optional[bool]=None,
        always: Optional[bool]=None
    ) -> str:
    """Clip a **copy** of `string` within `width` having
    `ending` as the final char(s).
    
    NOTE:
        If `force` then `ending` will be added
        no matter proper _positioning_.
        If `always` then `ending` will be added
        even if the string fits within the width."""
    w = min((_w := width or WIDTH), (
        l := len(e := ifNotNone(ending, PLACEHOLDER))
    )); n = max(_w - l, 0); _s = ifNotNone(string, STRING)
    if len(_s) < _w:
        if always:
            pass
        else:
            return _s
    elif not ifNotNone(force, FORCECLIP):
        return (s := _s[:n])[:n if (
            i := s.rfind(SPACECHAR)
        ) == -1 else i] + e[:w]
    return _s[:n] + e[:w]

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

def ifNotNone[A, B](a: A, b: B) -> A | B:
    "Self explanatory."
    return a if a is not None else b

def rstr(
        string: str,
        width:  int
    ) -> str:
    """Repeat a **copy** of `string` until the
    returned `str` is `width` in size."""
    return '' if width < 0 else ''.join(
        islice(cycle(string), width)
    )

def textalign3(
        string:    Optional[str_istr]=None,
        /,
        width:     Optional[int_iint]=None,
        fill:      Optional[str_istr]=None,
        border:    Optional[str_istr]=None,
        fromSide:  Optional[int_iint]=None,
        *,
        lfill:     Optional[str_istr]=None,
        rfill:     Optional[str_istr]=None,
        lborder:   Optional[str_istr]=None,
        rborder:   Optional[str_istr]=None,
        priority:  Optional[AT_iAT]  =None,
        alignment: Optional[AT_iAT]  =None
    ) -> str:
    """A rough and updated version of
    `textalign 3.0`'s text aligning where
    it's pretty much the same as `align`
    but implements `border`s and `Iterable`
    parameters.

    NOTE:
        `Iterable` parameters are used to reduce
        calls of `textalign3` so a desired multi-
        line output can be done in one go. Don't
        worry about `str`s being `Iterable`
        `textalign3` is smart enough to deal
        with them.
        `strs` is not used so any newlines within
        `string` are not dealt with.
        Uses `align`."""
    f  = ifNotNone(fill, FILL); b = ifNotNone(border, BORDER)
    s  = STRING; w = WIDTH; fs = FROMSIDE; lf = FILL; rf = FILL
    lb = BORDER; rb = BORDER; p = PRIORITY; a = ALIGNMENT; l = []
    for _s, _w, _f, _fs, _lf, _rf, _lb, _rb, _p, _a in zip_longest(
            __GSTRS__(ifNotNone(string, STRING)),
            __GINTS__(width or WIDTH),
            __GSTRS__(f),
            __GINTS__(fromSide or FROMSIDE),
            __GSTRS__(lfill or f),
            __GSTRS__(rfill or f),
            __GSTRS__(lborder or b),
            __GSTRS__(rborder or b),
            __GINTS__(ifNotNone(priority, PRIORITY)),
            __GINTS__(ifNotNone(alignment, ALIGNMENT))
        ):
        s  = _s if isinstance(_s, str) else s
        w  = _w or w
        f  = _f or f
        fs = ifNotNone(_fs, fs)
        lf = _lf or lf
        rf = _rf or rf
        lb = _lb or lb
        rb = _rb or rb
        p  = ifNotNone(_p, p)
        a  = ifNotNone(_a, a)
        t  = align(
            s, w - len(lb + rb), a, f, fs, p,
            lfill=lf, rfill=rf, strs=False
        )
        bw = (w - len(t)) / 2
        pi = [bw.__floor__(), bw.__ceil__()]
        if p == RIGHT:
            pi.reverse()
        l.append(
            rstr(lb, min(
                len(lb), pi[0]
            )) + t + rstr(rb, min(
                len(rb), pi[1]
            ))
        )
    return '\n'.join(l)

@strs
def wrap(
        string:    Optional[str]     =None,
        /,
        width:     Optional[int]     =None,
        key:       Optional[WrapFunc]=None,
        maxlines:  Optional[int]     =None,
        ending:    Optional[str]     =None,
        forceclip: Optional[bool]    =None
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
    k = key or __WRAP__; s = ''; L = len(_s := ifNotNone(string, STRING))
    w = width or WIDTH; ml = maxlines or MAXLINES
    j = l = 0; t0 = t1 = (-1, None)
    for i in range(1, L):
        b = ( t0 := (i, k(
            i, max(j, t1[0]), w, _s
        )) )[1] is not None
        if i - j == w:
            s0 = s1 = ''
            if (t := t0 if b else t1)[0] - j < 1:
                if _s[i].isalpha() and _s[i - 1].isalpha():
                    s0 = _s[j:i - 1]; s1 = '-\n'; j -= 1
                else:
                    s0 = _s[j:i]; s1 = '\n'
                j += w
            else:
                s0 = _s[j:t[0]]; j += t[0] - j
                for c in t[1]:
                    if c == NULLSTR:
                        return delback(s + s0 + s1)
                    s1 += c
            if 0 < ml <= (l := l + 1):
                return delback(s + clip(s0, w, ending, forceclip, True))
            s += s0 + s1
        elif b:
            t1 = tuple(t0)
    return delback(s + _s[j:])

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
        return 1
    def __repr__(self):
        return f'v{self.major}.{self.minor}'
version:     _version          = _version([5, 1])
__version__: str               = version.__repr__()
__all__:     list[str]         = [n for n in globals() if n[0] != '_']
### last update: July 29, 2026
