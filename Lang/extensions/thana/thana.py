from typing import Any, Dict, List, Tuple
import re

import aiofiles


class Thana:
    _user_def_fns: Dict[str, Any] = dict()
    _user_def_vars: Dict[str, Any] = dict()

    def __init__(self, *args, **kwargs) -> None:
        self._user_def_fns = dict()
        self._user_def_vars = dict()

    async def read_file(self, file: str, *, format='auto') -> str:
        async with aiofiles.open(file, 'r') as f:
            content = await f.read()

        return await self.apply_format(content)
        
    async def apply_format(self, content: str) -> str:
        print("Short:")
        replaced_short_content = await self.__apply_format(content, self.FormatFns._short_fn_call_re)
        return replaced_short_content
        # print("\nLong:")
        # return await self.__apply_format(replaced_short_content, self.FormatFns._long_fn_call_re)
    
    async def __apply_format(self, content: str, pattern: re.Pattern) -> str:
        has_shrunk = False

        reg_content_len = len(content)

        last_end = 0
        times_end_back = 0
        while (match := pattern.search(content)):
            content = await self.FormatFns._replace_fn(self, content, match)

            if (has_shrunk):
                has_shrunk = len(content) < reg_content_len
            reg_content_len = len(content)

            times_end_back += match.end() < last_end
            last_end = match.end()

            if (times_end_back == 100 and not has_shrunk):
                raise RecursionError("The formatting has been generating new formatting fns")

        return content


    class FormatFns:
        _short_fn_call_re = re.compile(r"^---[ \t]*([a-zA-Z_]\w*)[ \t]*(\$[a-zA-Z_]\w*|[^\n:]*?|\"[^\n:]*?\"|\'[^\n:]*?\')?[ \t]*(?:(?:[ \t]\(([ \t]*(?:\$[a-zA-Z_]\w*|[a-zA-Z_]\w*[ \t]*=[ \t]*:*?|.*?)?(?:[ \t]*,[ \t]*(?:\$[a-zA-Z_]\w*|[a-zA-Z_]\w*[ \t]*=.*?|.*?)?)*[ \t]*)\))?[ \t]*(?::[ \t]*(.+?)[ \t]*)?)?$", re.MULTILINE)
        _long_fn_call_re = re.compile(r"^---[ \t]*([a-zA-Z_]\w*)[ \t]*(\$[a-zA-Z_]\w*|[^\n:]*?|\"[^\n:]*?\"|\'[^\n:]*?\')?[ \t]*(?:[ \t]\(([ \t]*(?:\$[a-zA-Z_]\w*|[a-zA-Z_]\w*[ \t]*=[ \t]*:*?|.*?)?(?:[ \t]*,[ \t]*(?:\$[a-zA-Z_]\w*|[a-zA-Z_]\w*[ \t]*=.*?|.*?)?)*[ \t]*)\))?[ \t]*:\s*((?:.|\n)*?)\n---\s*$", re.MULTILINE)

        @classmethod
        async def _replace_fn(cls, odin: 'Thana', content: str, match: re.Match) -> str:
            fn_name, first_arg, args, text = match.groups()

            if (fn_name in cls.__dict__):
                fn = getattr(cls, fn_name)
            elif (fn_name in odin._user_def_fns):
                fn = odin._user_def_fns[fn_name]
            else:
                print(f"Warning: Unknown format function {fn_name}.")
                return content


            if (first_arg is not None and args is None and text is None):
                text = first_arg
                first_arg = None

            if (first_arg is not None or args is not None):
                args, kwargs = cls._parse_args(first_arg, args)
            else:
                args = []
                kwargs = {}

            print('#', args, kwargs, text, sep='; ')
            fn_result = await fn(odin, *args, **kwargs)(text)

            if (fn_result is not None):
                fn_result = str(fn_result)

            if (fn_result):
                # Return the content with the replacement based on match's start and end
                return content[:match.start()] + fn_result + content[match.end():]
            else:
                return content[:match.start()] + content[match.end()+1:]

        @classmethod
        def _parse_args(cls, first_arg: str, args: List[str]) -> Tuple[List[str], Dict[str, str]]:
            if first_arg is not None:
                if args is not None:
                    args = [first_arg, *args.split(',')]
                    first_arg = None
                else:
                    args = [first_arg]

            if args is None:
                args = []

            is_kwarg_re = re.compile(r"^\s*([a-zA-Z_]\w*)\s*=(?:\s*(?:\"|\'))?(.*?)(?:(?:\"|\')\s*)?$")

            new_args = []
            kwargs = {}
            for arg in args:
                match = is_kwarg_re.match(arg)
                if (match):
                    kwargs[match.group(1)] = match.group(2)
                else:
                    new_args.append(arg)

            return new_args, kwargs
        
        @classmethod
        def print(cls, odin: 'Thana', *args, **kwargs):
            async def _print(text):
                return print(*args, text, **kwargs)
            
            return _print
        
        @classmethod
        def split(cls, odin: 'Thana', *args, **kwargs):
            async def _split(text):
                return re.split(*args, text, **kwargs)
            
            return _split
        
        @classmethod
        def load(cls, odin: 'Thana', *args, **kwargs):
            async def _load(text):
                async with aiofiles.open(text, *args, **kwargs) as f:
                    return await f.read()
            
            return _load

        @classmethod
        def condition(cls, odin: 'Thana', *args, **kwargs):
            async def _condition(text):
                if all((eval(arg.strip()) for arg in args if arg.strip())):
                    return text
            
            return _condition
            
        # TODO: for

        @classmethod
        def repeat(cls, odin: 'Thana', *args, **kwargs):
            num_repeats = 2

            for arg in args:
                if (arg.isdigit()):
                    num_repeats = int(arg)
                    break

            async def _repeat(text):
                sep = kwargs.get('sep')

                print("Repeat:", text, sep, num_repeats)

                if (sep is None):
                    return text * num_repeats
                else:
                    return sep.join((text for _ in range(num_repeats)))
            
            return _repeat
        
        @classmethod
        def Py(cls, odin: 'Thana', *args, **kwargs):
            async def _Py(text):
                try:
                    return eval(text)
                except Exception as e:
                    return e
            return _Py

        # TODO: set
        # TODO: def

if __name__ == '__main__':
    import asyncio

    thana = Thana()

    test_result = asyncio.run(thana.read_file('./Lang/extensions/thana/thana_test.txt'))

    with open('./Lang/extensions/odin/thana_test.result', 'w+') as f:
        f.write(test_result)