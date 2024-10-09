from Lang.html.base_tag import BaseTag


class Dropdown(BaseTag):
    def __init__(self, id='text-editor-dropdown', *args, **kwargs):
        kwargs['style'] = {
            **kwargs.get('style', dict()),
            **{
                "position": "fixed",
                "bottom": "41%",
                "right": "10px",
                "width": "30%",
                "display": "none",
            }
        } 
        super().__init__('select', *args, id=id, **kwargs)

    def __repr__(self) -> str:
        return "<Dropdown>"
