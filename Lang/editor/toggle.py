from Lang.html.base_tag import BaseTag


class Toggle(BaseTag):
    def __init__(self, id='text-editor-toggle', *args, **kwargs): 
        kwargs['style'] = {
            **kwargs.get('style', dict()),
            **{
                "position": "fixed",
                "top": "10px",
                "right": "10px",
                "background-color": "#007bff",
                "color": "white",
                "padding": "10px",
                "border-radius": "5px",
                "cursor": "pointer",
            }
        } 
        super().__init__('input', *args, type='checkbox', id=id, **kwargs)

    def __repr__(self) -> str:
        return "<Toggle>"
