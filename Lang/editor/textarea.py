from Lang.html.base_tag import BaseTag


class TextArea(BaseTag):
    def __init__(self, id='text-editor-textarea', *args, **kwargs): 
        kwargs['style'] = {
            **kwargs.get('style', dict()),
            **{
                "position": "fixed",
                "bottom": "0",
                "right": "0",
                "width": "100%",
                "height": "40%",
                "background-color": "rgba(255, 255, 255, 0.9)",
                "border": "1px solid #ddd",
                "display": "none",
                "flex-direction": "column",
                "padding": "10px",
                "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
            }
        } 
        super().__init__('textarea', *args, id=id, **kwargs)

    def __repr__(self) -> str:
        return "<Textarea>"
