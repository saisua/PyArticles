from abc import abstractmethod

class Plugin:
    _is_plugin_setup: bool = False

    @abstractmethod
    async def setup(self, output_path, output_fname, doc: "Document") -> None:
        """
        Run the first time upon adding to the document
        """
        ...

    async def clear(self) -> None:
        """
        Run every time the document is remade
        """
        ...

    async def render(self, document: "Document", mode: str | int=None) -> None:
        """
        Run every time the document is rendered
        """
        ...