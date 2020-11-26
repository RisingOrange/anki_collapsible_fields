from aqt import mw

from aqt.gui_hooks import (
    webview_will_set_content,
    webview_did_receive_js_message,
)

from aqt.editor import Editor
from aqt.schema_change_tracker import ChangeTracker

from .utils import collapse_by_default_keyword


mw.addonManager.setWebExports(__name__, r'(web|icons)/.*\.(js|css|png)')


def load_collapsible_icon_js(webcontent, context):
    if isinstance(context, Editor):
        addon_package = context.mw.addonManager.addonFromModule(__name__)
        base_path = f'/_addons/{addon_package}/web'

        webcontent.css.append(f'{base_path}/collapsible.css')
        webcontent.js.append(f'{base_path}/collapsible.js')


def sticky_getter_and_setter(handled, message, context: Editor):
    cmd = message.split(':', 1)

    if cmd[0] in 'get_collapsed_by_default':
        model = context.note.model()
        idx = int(cmd[1])
        fld = model['flds'][idx]

        return (
            True,
            fld[collapse_by_default_keyword] if collapse_by_default_keyword in fld else False,
        )

    return handled


def init_webview():
    webview_will_set_content.append(load_collapsible_icon_js)
    webview_did_receive_js_message.append(sticky_getter_and_setter)